from __future__ import annotations

from typing import Any

from connect4.exceptions import InvalidMoveException
from connect4.players import Player


class Connect4Subscriber:
    def notify_board_updated(self, game, player, move):
        raise NotImplementedError

    def notify_game_result(self, result):
        raise NotImplementedError

    def notify_game_start(self, game):
        raise NotImplementedError


class Connect4:

    board: list[list[str]]
    players: dict[str, Player]
    _next_player: str
    _nrows: int
    _ncols: int
    subscribers: list[Connect4Subscriber]

    def __init__(self, player1: Player, player2: Player):
        self._nrows = 6
        self._ncols = 7
        self.board = [([" "] * self._nrows) for _ in range(self._ncols)]
        self._next_player = "x"
        self.subscribers = []

        self.players = dict(x=player1, o=player2)
        player1.init_game(self)
        player2.init_game(self)

    def subscribe(self, subscriber: Connect4Subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def play(self):
        for sub in self.subscribers:
            sub.notify_game_start(self)

        while self.is_undecided():
            player_label, turn_info = self.get_turn_info()
            player = self.players[player_label]

            move = player.get_next_move(self, self._next_player)
            while True:
                try:
                    self.apply_move(move)
                except InvalidMoveException:
                    player.handle_invalid_move(self, move)
                    move = player.get_next_move(self, self._next_player)
                else:
                    break
        for sub in self.subscribers:
            sub.notify_game_result(self, self._check_board())

    def apply_move(self, move):
        self.validate_move(move)
        self.update_board(move)
        self.end_turn()

    def _check_board(self):
        for i in range(self._ncols):
            for j in range(self._nrows):
                if self._check_slot(hint=(i, j)):
                    return self[i, j]
        if not any(slot == " " for col in self.board for slot in col):
            return "tied"
        return "undecided"

    def _check_slot(self, hint: tuple[int, int]) -> bool:
        candidate_label = self[*hint]
        if candidate_label == " ":
            return False
        # check vertical
        col, row_up = hint
        row_down = int(row_up)
        row_up += 1
        while row_up < self._nrows and self[col, row_up] == candidate_label:
            row_up += 1
        while row_down - 1 >= 0 and self[col, row_down - 1] == candidate_label:
            row_down -= 1
        if row_up - row_down >= 4:
            return True

        # check horizontal
        col_up, row = hint
        col_down = int(col_up)
        col_up += 1
        while col_up < self._ncols and self[col_up, row] == candidate_label:
            col_up += 1
        while col_down - 1 >= 0 and self[col_down - 1, row] == candidate_label:
            col_down -= 1
        if col_up - col_down >= 4:
            return True

        # check diagonal 1
        col, row = hint
        diff_up = 1
        diff_down = 0
        while (
            col + diff_up < self._ncols
            and row + diff_up < self._nrows
            and self[col + diff_up, row + diff_up] == candidate_label
        ):
            diff_up += 1
        while (
            col + diff_down - 1 >= 0
            and row + diff_down - 1 >= 0
            and self[col + diff_down - 1, row + diff_down - 1] == candidate_label
        ):
            diff_down -= 1
        if diff_up - diff_down >= 4:
            return True

        # check diagonal 2
        col, row = hint
        diff_up = 1
        diff_down = 0
        while (
            col + diff_up < self._ncols
            and row - diff_up >= 0
            and self[col + diff_up, row - diff_up] == candidate_label
        ):
            diff_up += 1
        while (
            col + diff_down - 1 > 0
            and row - (diff_down - 1) < self._nrows
            and self[col + diff_down - 1, row - (diff_down - 1)] == candidate_label
        ):
            diff_down -= 1

        if diff_up - diff_down >= 4:
            return True

        # default case
        return False

    def validate_move(self, move: int):
        "A valid move is a valid colum number and that column is not already full."
        if (
            not isinstance(move, int)
            or move < 0
            or move > self._ncols
            or self[move, -1] != " "
        ):
            raise InvalidMoveException

    def update_board(self, move: int):
        i = 0
        while self.board[move][i] != " ":
            i += 1
        self.board[move][i] = self._next_player

        for sub in self.subscribers:
            sub.notify_board_updated(self, self._next_player, move)

    def end_turn(self):
        self._next_player = "o" if self._next_player == "x" else "x"

    def get_turn_info(self) -> tuple[str, Any]:
        return self._next_player, self.board

    def is_undecided(self):
        return self._check_board() == "undecided"

    def __getitem__(self, idx):
        col, row = idx
        return self.board[col][row]
