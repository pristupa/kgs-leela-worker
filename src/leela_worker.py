import os
import subprocess
import tempfile
import time

from .logger import logger
from .settings import settings


class GameNotFoundError(Exception):
    pass


class LeelaWorker:

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def calculate_game(self, game_id: int):
        input_filepath = self._get_input_filepath(game_id)
        start_time = time.time()
        result = self._run_leela(game_id, input_filepath)
        time_spent = time.time() - start_time
        self._save_result(game_id, result, time_spent)

    def _run_leela(self, game_id: int, filepath: str) -> bytes:
        """
        :param game_id: Id of the game
        :param filepath: Path of a file for Leela to analyze (it's going to be deleted afterwards)
        :return: The contents of the Leela output file
        """
        logger.info(f"Running game id={game_id} from {filepath} with {settings['playouts']} playouts")
        result_filepath = settings['leela_output_file']
        leela_command = settings['leela_command'].replace('{INPUT}', filepath).replace('{OUTPUT}', result_filepath)
        subprocess.run(leela_command, shell=True, stdout=subprocess.PIPE)

        try:
            with open(result_filepath, 'rb') as result_file:
                result = result_file.read()
            os.unlink(result_filepath)
        finally:
            os.unlink(filepath)

        return result

    def _get_input_filepath(self, game_id: int) -> str:
        """
        Generates an SGF file with the game provided within the temp directory
        :param game_id: Id of the game
        :return: the absolute pathname of the created file
        """
        with self._db_connection as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT sgf_content FROM games WHERE id=%s', (game_id,))
                if cursor.rowcount == 0:
                    raise GameNotFoundError()
                sgf_content, = cursor.fetchone()
        file_descriptor, filepath = tempfile.mkstemp('.sgf')
        with open(file_descriptor, 'wb') as file:
            file.write(sgf_content)
        return filepath

    def _save_result(self, game_id: int, result: bytes, time_spent: float):
        with self._db_connection as connection:
            with connection.cursor() as cursor:
                result_data = {
                    'game_id': game_id,
                    'worker_tag': settings['worker_tag'],
                    'playouts': int(settings['playouts']),
                    'leela_result': result,
                    'time_spent': time_spent,
                }
                fields_names = ','.join(result_data.keys())
                placeholders = ','.join(['%s'] * len(result_data))
                fields_values = list(result_data.values())
                cursor.execute(f'INSERT INTO leela_results ({fields_names}) VALUES ({placeholders})', fields_values)
