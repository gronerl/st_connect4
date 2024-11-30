import random

class Game:
    
    def __str__():
        pass

class Connect4(GameState):
    def __init__(self):
        super().__init__()

    def __str__():
        pass

class InvalidMoveException(Exception):
    pass

class Player:
    def _raiseGameNotSupportedException(self, game: Game):
            errtxt = f'{self.__class__.__name__} does not implement playing the game {game.__class__.__name__}.'
            raise GameNotSupportedException(errtxt)
    
    def checkIsSupportedGame():
        raise NotImplementedError
    
    def getNextMove():
        raise NotImplementedError
    
    def setResultIsTied():
        pass

    def setResultIsWin():
        pass

    def setResultIsLose():
        pass
    
class ComputerPlayer(Player):
    def invalidMove(self, move):
        raise AssertionError("(╯°□°)╯︵ ┻━┻ It's a stupid game anyways.")

class RandomComputerPlayer(ComputerPlayer):
    def checkIsSupportedGame(self, game: Game):
        if not isinstance(game, Game):
            self._raiseGameNotSupportedException(game)
    
    def getNextMove(self, game: Game):
        moves = game.listValidMoves()
        move_idx = random.randint(0, len(moves)-1)
        return moves[move_idx]


class HumanConnect4Player(Player):
    def checkIsSupportedGame(self, game: Game):
        if not isinstance(game, Connect4):
            self._raiseGameNotSupportedException(game)
        
    def getNextMove(self, game:Game):
        print("The current board is:")
        print(str(game))
        while True:
            print("Please pick a column to drop your color:")
            try:
                move = int(input())
            except ValueError:
                print('Your input is not a valid integer.')
            else:
                break
        return move
    def setResultIsTied():
        print("The game ended in a tie.")
    
    def setResultIsWin():
        print("Congratulations, you win!")

    def setResultIsLose():
        print("You Lose. Better luck next time!")

class GameSession:
    
    game: Game
    players: list[Player]

    def play(self):
        while self.game.isUndecided():
            player_idx = self.game.next_player()
            player = self.players[player_idx]

            p.setBoard(self.game.state)
            move = player.getNextMove(self.game.state)
            while True:
                try:
                    self.game.applyMove(move)
                except InvalidMoveException:
                    player.invalidMove(move)
                    move = player.getNextMove(self.game.state)
                else:
                    break
            if self.rules.isDecided():
                break

        if self.game.isTied():
            for p in self.players:
                p.setResultIsTied()
        elif self.game.isWin():
            for p in self.players:
                p.setResultIsWin()



if __name__=="__main__":
    session = GameSession(Connect4, TextPlayer, RandomComputerPlayer)
    session.play()