"""module for StonehengeGame and StonehengeState class
"""
from typing import Dict, Any, List
import copy
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """A stonehenge game

    ===Attributes===
    length - side-length of a stonehenge grid
    rows - rows
    dowm_left - down-left diagonals
    down_right - down-right diagonals
    current_state - the state of a stonehenge game at a certain point in time
    """
    length: int
    rows: Dict[int, list]
    down_left: Dict[int, list]
    down_right: Dict[int, list]
    p1_score: int
    p2_score: int
    current_state: "StonehengeState"

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.

        Overrides Game.__init__
        """
        self.length = int(input("Enter the side length of the board: "))
        self.rows, self.down_left, self.down_right = {}, {}, {}
        letters, index_letter, num_cells = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 0, 2
        for i in range(self.length + 1):
            cells = []
            for _m in range(num_cells):
                cells.append(letters[index_letter])
                index_letter += 1
            self.rows[i] = ['n', cells]
            if num_cells > self.length:
                num_cells -= 1
            else:
                num_cells += 1
        for i in range(self.length + 1):
            cells = []
            for l in range(self.length):
                if i < len(self.rows[l][1]):
                    cells.append(self.rows[l][1][i])
            self.down_left[i] = ['n', cells]
        index = 1
        for c in self.rows[self.length][1]:
            self.down_left[index][1].append(c)
            index += 1
        for i in range(self.length + 1):
            cells = []
            for l in range(self.length):
                if -1 - i >= -len(self.rows[l][1]):
                    cells.append(self.rows[l][1][-1 - i])
            self.down_right[i] = ['n', cells]
        index = self.length
        for c in self.rows[self.length][1]:
            self.down_right[index][1].append(c)
            index -= 1
        self.current_state = StonehengeState(is_p1_turn,
                                             {'rows': self.rows,
                                              'left': self.down_left,
                                              'right': self.down_right}, [0, 0],
                                             self.length)

    def get_instructions(self) -> str:
        """
        Return the instructions for this Game.

        Overrides Game.get_instructions
        """
        return ("Players take turns claiming cells (labelled with a " +
                "capital\nletter). A ley-line (labelled with a '@') is " +
                "captured by a player\nwhen at least half of the cells " +
                "in the ley-line are captured by\nthe player. The first " +
                "player who captures at least half of the\nley-lines is " +
                "the winner. A ley-line, once claimed, cannot be\nclaimed " +
                "by the other player.")

    def is_over(self, state: "StonehengeState") -> bool:
        """
        Return whether or not this game is over at state.

        Overrides Game.is_over
        """
        half_ley_lines = 3 * (self.length + 1) / 2
        return (state.p1_score >= half_ley_lines
                or state.p2_score >= half_ley_lines)

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.

        Precondition: player is 'p1' or 'p2'.

        Overrides Game.is_winner
        """
        if self.is_over(self.current_state):
            return self.current_state.get_current_player_name() != player
        return False

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.

        Overrides Game.str_to_move
        """
        if not isinstance(string, str):
            return 'Invilid'
        return string.strip()


class StonehengeState(GameState):
    """The state of a stonehenge game at a certain point in time

    ===New Attributes===
    cur_board - what the stonehenge looks like currently
    p1_score - number of ley-lines captured by player 1
    p2_score - number of ley-lines captured by player 2
    length - side-length of a stonehenge grid
    """
    cur_board: Dict[str, Dict[int, list]]
    p1_score: int
    p2_score: int
    length: int

    def __init__(self, is_p1_turn: bool,
                 cur_board: Dict[str, Dict[int, list]], scores: List[int],
                 length: int) -> None:
        """Initialize this game state and set the current player based on
        is_p1_turn

        Extends GameState.__init__

        >>> a = StonehengeState(False, {}, [0, 1], 3)
        >>> a.p1_turn
        False
        >>> a.p2_score
        1
        """
        super().__init__(is_p1_turn)
        self.cur_board = cur_board.copy()
        self.p1_score, self.p2_score, self.length = scores[0], scores[1], length

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        Overrides GameState.__str__

        >>> rows = {0: ['2', ['A', '2']], 1: ['n', ['C', 'D', 'E']], \
        2: ['n', ['F', 'G', 'H', 'I']], 3: ['n', ['J', 'K', 'L']]}
        >>> left = {0: ['n', ['A', 'C', 'F']], \
        1: ['n', ['2', 'D', 'G', 'J']], 2: ['n', ['E', 'H', 'K']], \
        3: ['n', ['I', 'L']]}
        >>> right = {0: ['n', ['2', 'E', 'I']], \
        1: ['n', ['A', 'D', 'H', 'L']], 2: ['n', ['C', 'G', 'K']], \
        3: ['n', ['F', 'J']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [0, 1], 3)
        >>> print(a)
                            @       @
        <BLANKLINE>
                2       A       2       @
        <BLANKLINE>
            @       C       D       E       @
        <BLANKLINE>
        @       F       G       H       I
        <BLANKLINE>
            @       J       K       L       @
        <BLANKLINE>
                        @       @       @
        """
        space4, space7 = 4 * ' ', 7 * ' '
        result = self.length * space4 + ' '
        for i in range(2):
            result += space7 + self.val_ley_line(self.cur_board['left'][i])
        result += '\n\n'
        for i in range(self.length):
            result += (self.length - 1 - i) * space4
            result += self.val_ley_line(self.cur_board['rows'][i])
            for cell in self.cur_board['rows'][i][1]:
                result += space7 + cell
            if i + 2 <= self.length:
                result += space7
                result += self.val_ley_line(self.cur_board['left'][i + 2])
            result += '\n\n'
        result += space4
        result += self.val_ley_line(self.cur_board['rows'][self.length])
        for cell in self.cur_board['rows'][self.length][1]:
            result += space7 + cell
        result += space7 + self.val_ley_line(self.cur_board['right'][0])
        result += '\n\n' + 2 * space4 + ' '
        index = self.length
        while index > 0:
            result += space7 + self.val_ley_line(self.cur_board['right'][index])
            index -= 1
        return result

    def val_ley_line(self, ley_line: list) -> str:
        """Return a string representation of the value of ley_line

        >>> rows = {0: ['n', ['A', 'B']], 1: ['n', ['C', 'D', '1']], \
        2: ['n', ['F', 'G']]}
        >>> left = {0: ['n', ['A', 'C']], 1: ['n', ['B', 'D', 'F']], \
        2: ['1', ['1', 'G']]}
        >>> right = {0: ['1', ['B', '1']], 1: ['n', ['A', 'D', 'G']], \
        2: ['n', ['C', 'F']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [2, 0], 2)
        >>> a.val_ley_line(a.cur_board['left'][2])
        '1'
        >>> a.val_ley_line(a.cur_board['right'][1])
        '@'
        """
        if ley_line[0] == 'n':
            return '@'
        return ley_line[0]

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.

        Overrides GameState.get_possible_moves

        >>> rows = {0: ['2', ['A', '2']], 1: ['n', ['C', 'D', 'E']], \
        2: ['n', ['F', 'G', 'H', '1']], 3: ['n', ['J', 'K', '2']]}
        >>> left = {0: ['n', ['A', 'C', 'F']], \
        1: ['n', ['2', 'D', 'G', 'J']], 2: ['n', ['E', 'H', 'K']], \
        3: ['1', ['1', '2']]}
        >>> right = {0: ['n', ['2', 'E', '1']], \
        1: ['n', ['A', 'D', 'H', '2']], 2: ['n', ['C', 'G', 'K']], \
        3: ['n', ['F', 'J']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [1, 1], 3)
        >>> a.get_possible_moves()
        ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']
        >>> rows = {0: ['1', ['1', 'B']], 1: ['n', ['C']]}
        >>> left = {0: ['1', ['1']], 1: ['n', ['B', 'C']]}
        >>> right = {0: ['n', ['B']], 1: ['1', ['1', 'C']]}
        >>> b = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [3, 0], 1)
        >>> b.get_possible_moves()
        []
        """
        half_ley_lines = 3 * (self.length + 1) / 2
        if self.p1_score >= half_ley_lines or self.p2_score >= half_ley_lines:
            return []
        result = []
        for index in self.cur_board['rows']:
            for cell in self.cur_board['rows'][index][1]:
                if cell != '1' and cell != '2':
                    result.append(cell)
        return result

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the GameState that results from applying move to this GameState.

        Overrides GameState.make_move

        >>> rows = {0: ['2', ['A', '2']], 1: ['n', ['C', 'D', 'E']], \
        2: ['n', ['F', 'G', 'H', '1']], 3: ['n', ['J', 'K', '2']]}
        >>> left = {0: ['n', ['A', 'C', 'F']], \
        1: ['n', ['2', 'D', 'G', 'J']], 2: ['n', ['E', 'H', 'K']], \
        3: ['1', ['1', '2']]}
        >>> right = {0: ['n', ['2', 'E', '1']], \
        1: ['n', ['A', 'D', 'H', '2']], 2: ['n', ['C', 'G', 'K']], \
        3: ['n', ['F', 'J']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [1, 1], 3)
        >>> m = a.make_move('G')
        >>> m.cur_board['left'][1][0] == '2'
        True
        >>> m.p2_score == 2
        True
        >>> m.p1_turn
        True
        >>> a.cur_board['left'][1][0] == 'n'
        True
        >>> a.p2_score == 1
        True
        >>> print(m)
                            @       2
        <BLANKLINE>
                2       A       2       @
        <BLANKLINE>
            @       C       D       E       1
        <BLANKLINE>
        @       F       2       H       1
        <BLANKLINE>
            @       J       K       2       @
        <BLANKLINE>
                        @       @       @
        """
        board = copy.deepcopy(self.cur_board)
        cur_player = '1'
        scores = [self.p1_score, self.p2_score]
        if not self.p1_turn:
            cur_player = '2'
        for lines in board:
            for line in board[lines]:
                states = board[lines][line]
                self.move_to_board(scores, states, move, cur_player)
        return StonehengeState(cur_player == '2', board, scores, self.length)

    def move_to_board(self, player_scores: List[int], cur_states: list,
                      move: str, cur_player: str) -> None:
        """Capture cell in cur_state by cur_player if there is such a
        cell == move. If >= half of the cells in cur_state are captured, add 1
        score to player_score

        >>> rows = {0: ['2', ['A', '2']], 1: ['n', ['C', 'D', 'E']], \
        2: ['n', ['F', '2', 'H', '1']], 3: ['n', ['J', 'K', '2']]}
        >>> left = {0: ['n', ['A', 'C', 'F']], \
        1: ['2', ['2', 'D', '2', 'J']], 2: ['n', ['E', 'H', 'K']], \
        3: ['1', ['1', '2']]}
        >>> right = {0: ['n', ['2', 'E', '1']], \
        1: ['n', ['A', 'D', 'H', '2']], 2: ['n', ['C', '2', 'K']], \
        3: ['n', ['F', 'J']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [1, 1], 3)
        >>> c = ['n', ['C', '2', 'E']]
        >>> b = a.move_to_board([1, 0], c, 'E', '2')
        >>> b is None
        True
        >>> c == ['2', ['C', '2', '2']]
        True
        """
        scores = player_scores
        states = cur_states
        for cell in range(len(states[1])):
            if states[1][cell] == move:
                states[1][cell] = cur_player
                if (states[0] == 'n'
                        and states[1].count(cur_player) >= len(states[1]) / 2
                        and cur_player == '2'):
                    states[0] = '2'
                    scores[1] += 1
                elif (states[0] == 'n'
                      and states[1].count(cur_player) >= len(states[1]) / 2):
                    states[0] = '1'
                    scores[0] += 1

    def __repr__(self) -> Any:
        """
        Return a representation of this state (which can be used for
        equality testing).

        Overrides GameState.__repr__
        """
        return "P1's Turn: {}\nImage: \n{}".format(self.p1_turn,
                                                   self.__str__())

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        Overrides GameState.rough_outcome

        >>> rows = {0: ['1', ['1', 'B']], 1: ['n', ['C', 'D', 'E']], \
        2: ['n', ['F', 'G']]}
        >>> left = {0: ['1', ['1', 'C']], 1: ['n', ['B', 'D', 'F']], \
        2: ['n', ['E', 'G']]}
        >>> right = {0: ['n', ['B', 'E']], 1: ['n', ['1', 'D', 'G']], \
        2: ['n', ['C', 'F']]}
        >>> a = StonehengeState(False, \
        {'rows': rows, 'left': left, 'right': right}, [2, 0], 2)
        >>> a.rough_outcome()
        0
        >>> b = a.make_move('G')
        >>> b.rough_outcome()
        0
        >>> a = b.make_move('D')
        >>> a.rough_outcome()
        -1
        >>> b = a.make_move('F')
        >>> b.rough_outcome()
        1
        """
        half_ley_lines = 3 * (self.length + 1) / 2
        if self.get_possible_moves() == []:
            return self.LOSE
        other_win = True
        for move in self.get_possible_moves():
            state = self.make_move(move)
            if (state.p1_score >= half_ley_lines
                    or state.p2_score >= half_ley_lines):
                return self.WIN
            elif all([(state.make_move(x).p1_score < half_ley_lines
                       and state.make_move(x).p2_score < half_ley_lines)
                      for x in state.get_possible_moves()]):
                other_win = False
        if other_win:
            return self.LOSE
        return self.DRAW


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
