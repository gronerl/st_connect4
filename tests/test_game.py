import pytest

from connect4.game import Connect4
from connect4.players import RandomConnect4ComputerPlayer
from connect4.terminal import Connect4TextTerminal

tied_board = """+0123456+
|oooxooo|
|xxxoxxx|
|oooxooo|
|xxxoxxx|
|oooxooo|
|xxxoxxx|
+-------+
"""

empty_board = """+0123456+
|       |
|       |
|       |
|       |
|       |
|       |
+-------+
"""
win_bl_vert = """+0123456+
|       |
|       |
|x      |
|x      |
|x      |
|x      |
+-------+
"""
win_bl_hor = """+0123456+
|       |
|       |
|       |
|       |
|       |
|xxxx   |
+-------+
"""
win_bl_diag = """+0123456+
|       |
|       |
|   x   |
|  x    |
| x     |
|x      |
+-------+
"""
win_tl_vert = """+0123456+
|x      |
|x      |
|x      |
|x      |
|       |
|       |
+-------+
"""
win_tl_hor = """+0123456+
|xxxx   |
|       |
|       |
|       |
|       |
|       |
+-------+
"""
win_tl_diag = """+0123456+
|x      |
| x     |
|  x    |
|   x   |
|       |
|       |
+-------+
"""


def str_to_board(board_str):
    board_str = board_str.strip()
    rows = board_str.split("\n")
    n_cols = len(rows[0]) - 2
    res = [list() for _ in range(n_cols)]
    for row in reversed(rows[1:-1]):
        for col, char in enumerate(row[1:-1]):
            res[col].append(char)
    return res


def test_str_to_board():

    c4 = Connect4(RandomConnect4ComputerPlayer(), RandomConnect4ComputerPlayer())

    tt = Connect4TextTerminal()

    c4.board = str_to_board(tied_board)
    print(c4.board)
    cand = tt._board_to_str(c4)

    print(cand)
    assert tied_board.strip() == cand


class TestConnect4CheckSlot:
    @pytest.mark.parametrize(
        ["board_str", "hint"],
        [
            (win_bl_diag, (0, 0)),
            (win_bl_diag, (2, 2)),
            (win_bl_diag, (3, 3)),
            (win_bl_hor, (0, 0)),
            (win_bl_vert, (0, 0)),
            (win_tl_diag, (0, 5)),
            (win_tl_hor, (0, 5)),
            (win_tl_vert, (0, 5)),
        ],
    )
    def test_winning_x(self, board_str, hint):
        c4 = Connect4(RandomConnect4ComputerPlayer(), RandomConnect4ComputerPlayer())
        c4.board = str_to_board(board_str)
        assert c4._check_slot(hint=hint)
