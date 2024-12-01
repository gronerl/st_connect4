from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from connect4.exceptions import GameNotSupportedException

if TYPE_CHECKING:
    from connect4.play import Connect4


class Player:
    def _raise_game_not_supported_exception(self, game: Any):
        errtxt = f"{self.__class__.__name__} does not implement playing the game {game.__class__.__name__}."
        raise GameNotSupportedException(errtxt)

    def ccheck_is_supported_game(self, game: Any):
        raise NotImplementedError

    def get_next_move(self, game, player):
        raise NotImplementedError

    def handle_invalid_move(self, game, move):
        raise NotImplementedError


class ComputerPlayer(Player):
    def handle_invalid_move(self, game: "Connect4", move: int):
        raise AssertionError("(╯°□°)╯︵ ┻━┻ It's a stupid game anyways.")


class RandomComputerPlayer(ComputerPlayer):
    def check_is_supported_game(self, game: Any):
        from connect4.play import Connect4

        if not isinstance(game, Connect4):
            self._raise_game_not_supported_exception(game)

    def list_valid_moves(self, game):
        res = list()
        for i, col in enumerate(game.board):
            if col[-1] == " ":
                res.append(i)
        return res

    def get_next_move(self, game: "Connect4", player):
        moves = self.list_valid_moves(game)
        move_idx = random.randint(0, len(moves) - 1)
        return moves[move_idx]


class HumanConnect4Player(Player):
    def __init__(self, io_provider):
        super().__init__()
        self.terminal = io_provider

    def init_game(self, game: "Connect4"):
        game.subscribe(self.terminal)

    def check_is_supported_game(self, game: Connect4):
        if not isinstance(game, Connect4):
            self._raise_game_not_supported_exception(game)

    def get_next_move(self, game, player):
        return self.terminal.get_next_move(game, player)

    def handle_invalid_move(self, game, move):
        self.terminal.handle_invalid_move(game, move)
