import os
import tempfile

from .logger import logger
from .settings import settings


class GameNotFoundError(Exception):
    pass


class LeelaWorker:

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def calculate_game(self, game_id: int):
        input_filepath = self._get_input_filepath(game_id)
        result = self._run_leela(game_id, input_filepath)
        self._save_result(game_id, result)

    def _run_leela(self, game_id: int, filepath: str) -> bytes:
        """
        :param game_id: Id of the game
        :param filepath: Path of a file for Leela to analyze (it's going to be deleted afterwards)
        :return: The contents of the Leela output file
        """
        logger.info(f"Running game id={game_id} from {filepath} with {settings['playouts']} playouts")
        result_filepath = '/path/to/leela/result.sgf'  # TODO: Replace with the output file path

        raise NotImplementedError('Run Leela is not implemented')  # TODO: Replace this line with the actual Leela run

        with open(result_filepath, 'rb') as result_file:
            result = result_file.read()
        os.unlink(filepath)
        os.unlink(result_filepath)

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

    def _save_result(self, game_id: int, result: bytes):
        with self._db_connection as connection:
            with connection.cursor() as cursor:
                result_data = {
                    'game_id': game_id,
                    'worker_tag': settings['worker_tag'],
                    'playouts': settings['playouts'],
                    'leela_result': result,
                }
                fields_names = ','.join(result_data.keys())
                placeholders = ','.join(['%s'] * len(result_data))
                fields_values = list(result_data.values())
                cursor.execute(f'INSERT INTO leela_results ({fields_names}) VALUES ({placeholders})', fields_values)
