import os.path
from .settings import settings


class LeelaWorker:

    def __init__(self):
        pass

    def calculate_game(self, game_id: int):
        sgf_directory = settings.sgf_dir
        filename = f'kgs-crawler-{game_id}.sgf'
        filepath = os.path.join(sgf_directory, filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'File {filename} not found in {sgf_directory}')
        self._run_leela(filepath)

    def _run_leela(self, filepath: str):
        raise NotImplementedError('Run Leela command is not implemented')
