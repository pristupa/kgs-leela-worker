import os
import re
import subprocess
import tempfile
import time
from typing import TYPE_CHECKING

from .logger import logger
from .settings import settings

if TYPE_CHECKING:
    from .database import Database


class GameNotFoundError(Exception):
    pass


class LeelaWorker:
    leela_output_regexp = re.compile(r'(\d+)/(\d+)')

    def __init__(self, db: 'Database'):
        self._db = db

    def calculate_game(self, game_id: int, kilo_playouts: int):
        input_filepath = self._get_input_filepath(game_id)
        start_time = time.time()
        result = self._run_leela(game_id, input_filepath, kilo_playouts)
        time_spent = time.time() - start_time
        self._save_result(game_id, result, time_spent, kilo_playouts)

    def _run_leela(self, game_id: int, filepath: str, kilo_playouts: int) -> bytes:
        """
        :param game_id: Id of the game
        :param filepath: Path of a file for Leela to analyze (it's going to be deleted afterwards)
        :return: The contents of the Leela output file
        """
        playouts = kilo_playouts * 1000
        logger.info(f"Running game id={game_id} from {filepath} with {playouts} playouts")
        result_filepath = settings['leela_output_file']

        subprocess.run([
            settings['python_bin'],
            settings['python_leela'],
            '--file', filepath,
            '--output', result_filepath,
            '--profiles', f'{kilo_playouts}k',
            '--verbose', '1',
            '--force',
            '--no_append',
        ])

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
        cursor = self._db.execute('SELECT sgf_content FROM games WHERE id=%s', (game_id,))
        if cursor.rowcount == 0:
            raise GameNotFoundError()
        sgf_content, = cursor.fetchone()
        file_descriptor, filepath = tempfile.mkstemp('.sgf')
        with open(file_descriptor, 'wb') as file:
            file.write(sgf_content)
        return filepath

    def _save_result(self, game_id: int, result: bytes, time_spent: float, kilo_playouts: int):
        result_data = {
            'game_id': game_id,
            'worker_tag': settings['worker_tag'],
            'playouts': kilo_playouts * 1000,
            'leela_result': result,
            'time_spent': time_spent,
        }
        fields_names = ','.join(result_data.keys())
        placeholders = ','.join(['%s'] * len(result_data))
        fields_values = list(result_data.values())
        self._db.execute(f'INSERT INTO leela_results ({fields_names}) VALUES ({placeholders})', fields_values)
