from connect4.game import Connect4Subscriber
from connect4.players import ComputerPlayer


class Connect4TextTerminal(Connect4Subscriber):
    def _print_board(self, game):
        board_strs = ["+"] + [str(i) for i in range(game._ncols)] + ["+", "\n"]
        for i in range(game._nrows):
            board_strs += "|"
            for j in range(game._ncols):
                board_strs += game[j, -1 - i]
            board_strs += "|\n"
        board_strs += ["+"] + ["-"] * game._ncols + ["+"]
        print("".join(board_strs))

    def notify_board_updated(self, game, player, move):
        if isinstance(game.players[player], ComputerPlayer):
            print(f"The computer places a chip in column {move}.")
        else:
            print(f"You chose to drop a chip in column {move}.")

        print("The board now looks like this:")

        self._print_board(game)

    def notify_game_result(self, game, result):
        if result == "tied":
            print("The game ended in a tie.")
        elif result in game.players:
            if isinstance(game.players[result], ComputerPlayer):
                print("You Lose. Better luck next time!")
            else:
                print("Congratulations, you win!")
        else:
            err_str = f"The game result '{result}' is not supported."
            raise NotImplementedError(err_str)

    def notify_game_start(self, game):
        print("Welcome to Connect4!")
        self._print_board(game)

    def handle_invalid_move(self, game, move):
        print(f"Column {move} is not a valid move.")

    def get_next_move(self, game, player):

        while True:
            msg = "Please pick a column to drop your chip."
            msg += f"(You are '{player}'):"
            print(msg)
            try:
                move = int(input())
            except ValueError:
                print("Your input is not a valid integer.")
            else:
                break
        return move
