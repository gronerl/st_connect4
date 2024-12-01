import io
from typing import Iterable

from connect4.game import Connect4Subscriber
from connect4.players import ComputerPlayer


class Connect4TextTerminal(Connect4Subscriber):
    """
    This class implements i/o for a human player of the connect four game.
    There are two main access paths: Player classes directly invoking i/o or game status updates
    through the Connect4Subscriber interface. Rationale is that in case of multiple players,
    moves are per player, while e.g. updating the board and announcing the game result are
    broadcast to all players.
    """

    def _read(self, *args, **kwargs):
        "Wrapper around input() to facilitate overriding in mock class for testing."
        return input(*args, **kwargs)

    def _write(self, *args, **kwargs):
        "Wrapper around print() to facilitate overriding as mock class for testing."
        print(*args, **kwargs)

    def _board_to_str(self, game):
        "Represent game board as string with a frame and column numbers."
        # first, header line
        board_strs = ["+"] + [str(i) for i in range(game.ncols)] + ["+", "\n"]
        # for each row, add first and last a frame literal '|' and the row of the board.
        # The game board is stored in a permuted fashion (a list per column), making
        # list comprehensions or e.g. string join methods unfeasible.
        for i in range(game.nrows):
            board_strs += "|"
            for j in range(game.ncols):
                board_strs += game[j, -1 - i]
            board_strs += "|\n"
        # finally, add closing frame
        board_strs += ["+"] + ["-"] * game.ncols + ["+"]
        return "".join(board_strs)

    def _print_board(self, game):
        self._write(self._board_to_str(game))

    def notify_board_updated(self, game, player, move):
        """Called by Connect4 class, when a move is accepted and the board is updated.
        This is conveyed to the user with a short message and the updated board."""
        if isinstance(game.players[player], ComputerPlayer):
            self._write(f"The computer places a chip in column {move}.")
        else:
            self._write(f"You chose to drop a chip in column {move}.")

        self._write("The board now looks like this:")

        self._print_board(game)

    def notify_game_result(self, game, result):
        """Called by Connect4 class, when the game has ended.
        Announces the winner (or a draw) to the user."""
        if result == "tied":
            self._write("The game ended in a tie.")
        elif result in game.players:
            if isinstance(game.players[result], ComputerPlayer):
                self._write("You Lose. Better luck next time!")
            else:
                self._write("Congratulations, you win!")
        else:
            err_str = f"The game result '{result}' is not supported."
            raise NotImplementedError(err_str)

    def notify_game_start(self, game):
        """Called by Connect4 class, at the beginning of program execution.
        print the (empty) board."""
        self._write("Welcome to Connect4!")
        self._print_board(game)

    def handle_invalid_move(self, game, move):
        """Called by Player classes to let the user know that his chosen move was invalid."""
        self._write(f"Column {move} is not a valid move.")

    def get_next_move(self, game, player):
        """Asks the user to specify a column to drop the chip, checks if it is a valid integer."""

        # repeatedly ask for input until an integer is specified
        while True:
            msg = "Please pick a column to drop your chip."
            msg += f"(You are '{player}'):"
            self._write(msg)
            try:
                move = int(self._read())
            except ValueError:
                self._write("Your input is not a valid integer.")
            else:
                break
        return move


class CapturedConnect4TextTerminal(Connect4TextTerminal):
    """Wrapper to enable intercepting of output to string."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.str_strm = io.StringIO()

    def _write(self, *args, **kwargs):
        print(*args, **kwargs, file=self.str_strm)


class MockInputConnect4TextTerminal(Connect4TextTerminal):
    """Wrapper to enable feeding mock moves to the game for testing."""

    def __init__(self, *args, mock_input_strs: Iterable[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if mock_input_strs is not None:
            self.mock_input_iter = iter(mock_input_strs)
        else:
            self.mock_input_iter = iter([])

    def set_inputs(self, mock_input_strs: Iterable[str]):
        self.mock_input_iter = iter(mock_input_strs)

    def _read(self, *args, **kwargs):
        return next(self.mock_input_iter)


class CapturedMockInputConnect4TextTerminal(
    CapturedConnect4TextTerminal, MockInputConnect4TextTerminal
):
    """Mock wrapper to enable intercepting both input and output"""

    pass
