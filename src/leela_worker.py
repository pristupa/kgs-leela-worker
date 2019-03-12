import os.path

from .settings import settings
from .logger import logger


class LeelaWorker:

    def __init__(self, db_connection):
        self._db_connection = db_connection

    def calculate_game(self, game_id: int):
        input_filepath = self._get_input_filepath(game_id)
        result_filepath = self._run_leela(game_id, input_filepath)
        self._save_result(game_id, result_filepath)

    def _run_leela(self, game_id: int, filepath: str) -> str:
        """
        :param game_id: Id of the game
        :param filepath: Path of a file for Leela to analyze
        :return: Path of the Leela output file
        """
        logger.info(f'Running game id={game_id} from {filepath} with {settings.playouts} playouts')
        raise NotImplementedError('Run Leela command is not implemented')  # TODO: Remove this line
        return filepath  # TODO: Replace with the output file path

    def _get_input_filepath(self, game_id: int) -> str:
        filename = f'kgs-crawler-{game_id}.sgf'
        filepath = os.path.join(settings.sgf_dir, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'File {filename} not found in {settings.sgf_dir}')
        return filepath

    def _save_result(self, game_id: int, result_filepath: str):
        with open(result_filepath, 'rb') as result_file:
            result = result_file.read()
        with self._db_connection as connection:
            with connection.cursor() as cursor:
                result_data = {
                    'game_id': game_id,
                    'worker_tag': settings.worker_tag,
                    'playouts': settings.playouts,
                    'leela_result': result,
                }
                fields_names = ','.join(result_data.keys())
                placeholders = ','.join(['%s'] * len(result_data))
                fields_values = list(result_data.values())
                cursor.execute(f'INSERT INTO leela_results ({fields_names}) VALUES ({placeholders})', fields_values)
