from __future__ import annotations

from typing import Any

from connect4.exceptions import InvalidMoveException
from connect4.players import Player


class Connect4Subscriber:
    def notify_board_updated(self, game, player, move):
        """Invoked whenever a move is accepted and the board was updated."""
        raise NotImplementedError

    def notify_game_result(self, result):
        """Invoked when the game is decided (a winner is found or the game ends in a draw)."""
        raise NotImplementedError

    def notify_game_start(self, game):
        """Invoked when the game is started."""
        raise NotImplementedError


class Connect4:
    """This class holds the state and state transitions of a classic connect four game.
    In addition, it provides a mechanism to subscribe on updates of the game progress.
    """

    board: list[list[str]]
    players: dict[str, Player]
    _next_player: str
    _nrows: int
    _ncols: int
    subscribers: list[Connect4Subscriber]

    def __init__(self, player1: Player, player2: Player):
        "Provide any 2 players implementing strategies for the connect 4 game."
        self._nrows = 6
        self._ncols = 7
        self.board = [([" "] * self._nrows) for _ in range(self._ncols)]
        self._next_player = "x"
        self.subscribers = []

        self.players = dict(x=player1, o=player2)
        player1.init_game(self)
        player2.init_game(self)

    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return self._nrows

    def subscribe(self, subscriber: Connect4Subscriber):
        """Add an object that inherits from Connect4Subscriber to the list of subscribers.
        If the same instance is already present, no action is done."""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def play(self):
        """Main driver function of the game. Invoking this runs the game start-to-end."""
        # first, notify subscribers of the start of the game (allowing e.g. to print the empty board)
        for sub in self.subscribers:
            sub.notify_game_start(self)

        # keep playing until the game is decided.
        while self._is_undecided():
            # get current player and the board for passing on to players
            player_label, turn_info = self._get_turn_info()

            player = self.players[player_label]

            # query player for next move and handle invalid moves. (Keep querying until input is valid.)
            move = player.get_next_move(self, self._next_player)
            while True:
                try:
                    # if valid, this also triggers updating the subscribers.
                    self._apply_move(move)
                except InvalidMoveException:
                    # Notify player that move was invalid, e.g. so he can inform the user
                    player.handle_invalid_move(self, move)
                    # query move again
                    move = player.get_next_move(self, self._next_player)
                else:
                    break
        # notify subscribers of end of game (allowing e.g. to announce a winner/draw)
        result = self._check_board()
        for sub in self.subscribers:
            sub.notify_game_result(self, result)

    def _apply_move(self, move):
        self._validate_move(move)
        self._update_board(move)
        self._end_turn()

    def _check_board(self):
        # loop over all slots of the game board and check if it is part of a winning connection
        # if yes, return the label as the winner.
        for i in range(self._ncols):
            for j in range(self._nrows):
                if self._check_slot(hint=(i, j)):
                    return self[i, j]

        # if there are no winning connections, check if the board is fully filled and therefore tied
        if not any(slot == " " for col in self.board for slot in col):
            return "tied"

        # otherwise the game is not yet decided.
        return "undecided"

    def _check_slot(self, hint: tuple[int, int]) -> bool:
        # check vertical, horizontal, diagonals (left-to-right ascending, ltr descending)
        # by walking forwards and backwards as far as the symbols are the same. The length
        # of a connection is given by the index difference of either end.
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

    def _validate_move(self, move: int):
        # A valid move is a valid colum number and that column is not already full.
        # if a column is full, the top element is no longer empty (self[move, -1] != " ")
        if (
            not isinstance(move, int)
            or move < 0
            or move > self._ncols
            or self[move, -1] != " "
        ):
            raise InvalidMoveException

    def _update_board(self, move: int):

        # find lowest free slot by searching from bottom
        i = 0
        while self.board[move][i] != " ":
            i += 1
        # write player label to lowest free slot
        self.board[move][i] = self._next_player

        # notify subscribers of the changed board
        for sub in self.subscribers:
            sub.notify_board_updated(self, self._next_player, move)

    def _end_turn(self):
        # toggle between "x" and "o" as current players
        self._next_player = "o" if self._next_player == "x" else "x"

    def _get_turn_info(self) -> tuple[str, Any]:
        return self._next_player, self.board

    def _is_undecided(self) -> bool:
        return self._check_board() == "undecided"

    def __getitem__(self, idx):
        # convenience to allow 2d index directly on Connect4 objects
        col, row = idx
        return self.board[col][row]
