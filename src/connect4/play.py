from connect4.game import Connect4
from connect4.players import HumanConnect4Player, RandomConnect4ComputerPlayer
from connect4.terminal import Connect4TextTerminal


def play():
    terminal = Connect4TextTerminal()
    session = Connect4(HumanConnect4Player(terminal), RandomConnect4ComputerPlayer())
    # session = Connect4(HumanConnect4Player(RandomConnect4ComputerPlayer()), RandomConnect4ComputerPlayer())
    # session = Connect4(HumanConnect4Player(terminal), HumanConnect4Player(terminal))
    session.play()


if __name__ == "__main__":
    play()
