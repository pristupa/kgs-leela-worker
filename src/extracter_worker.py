import sys
from typing import TYPE_CHECKING

from .leela_worker import LeelaWorker

if TYPE_CHECKING:
    from .database import Database


class ExtracterWorker(LeelaWorker):

    def __init__(self, db: 'Database', games_count: int):
        super().__init__(db)
        self._games_count = games_count

    def calculate_game(self, game_id: int, kilo_playouts: int):
        self._games_count -= 1
        if self._games_count < 0:
            sys.exit()
        self._get_input_filepath(game_id)

    def _write_sgf_content(self, game_id: int, sgf_content: bytes) -> str:
        filepath = f'./games/{game_id}.sgf'
        with open(filepath, 'wb') as file:
            file.write(sgf_content)
        return filepath
