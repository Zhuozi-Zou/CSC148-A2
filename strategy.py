"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, List, Union
from game import Game
from game_state import GameState


class Stack:
    """
    Last-in, first-out (LIFO) stack.

    This code is from lab 3
    """

    def __init__(self) -> None:
        """
        Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contents = []

    def add(self, obj: Union[object, 'Tree']) -> None:
        """
        Add object obj to top of Stack self.

        >>> s = Stack()
        >>> s.add(7)
        """
        self._contents.append(obj)

    def remove(self) -> Union[object, 'Tree']:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty.

        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        return self._contents.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(7)
        >>> s.is_empty()
        False
        """
        return len(self._contents) == 0


class Tree:
    """Represent a tree

    ===Attributes===
    children - a list of children of a tree
    value - the value of a tree
    score - the score of a tree
    """
    value: Union[object, GameState]
    children: List['Tree']
    score: int

    def __init__(self, value: Union[object, GameState] = None,
                 children: List['Tree'] = None, score: int = None) -> None:
        """Initialize a tree with its value and children

        >>> a = Tree(3)
        >>> a.value
        3
        >>> a.children
        []
        """
        self.value = value
        self.children = children.copy() if children else []
        self.score = score


def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def minimax_recursive(game: Game) -> Any:
    """Return the strongest possible move of the current state of game
    recursively

    Assume game is not over
    """
    old_state = game.current_state
    scores_possible_moves = [(-1 * max_score(game, old_state.make_move(x)))
                             for x in old_state.get_possible_moves()]
    index = scores_possible_moves.index(max(scores_possible_moves))
    game.current_state = old_state
    return old_state.get_possible_moves()[index]


def max_score(game: Game, state: GameState) -> int:
    """Return the score of state if game is over, otherwise return the max
    score of moves of state
    """
    game.current_state = state
    if game.is_over(state):
        if state.p1_turn:
            if game.is_winner('p1'):
                return 1
            elif game.is_winner('p2'):
                return -1
            return 0
        else:
            if game.is_winner('p2'):
                return 1
            elif game.is_winner('p1'):
                return -1
            return 0
    else:
        return max([(-1 * max_score(game, state.make_move(x)))
                    for x in state.get_possible_moves()])


def minimax_iterative(game: Game) -> Any:
    """Return the strongest possible move of the current state of game
    iteratively

    Assume game is not over
    """
    old_state = game.current_state
    process, state = Stack(), Tree(old_state)
    process.add(state)

    while not process.is_empty():
        tree = process.remove()
        game.current_state = tree.value
        if game.is_over(game.current_state):
            if not(game.is_winner('p1') or game.is_winner('p2')):
                tree.score = 0
            elif game.current_state.p1_turn and game.is_winner('p1'):
                tree.score = 1
            elif game.current_state.p1_turn and game.is_winner('p2'):
                tree.score = -1
            elif (not game.current_state.p1_turn) and game.is_winner('p2'):
                tree.score = 1
            else:
                tree.score = -1
        elif tree.children == []:
            for move in game.current_state.get_possible_moves():
                next_state = Tree(game.current_state.make_move(move))
                tree.children.append(next_state)
            process.add(tree)
            for child in tree.children:
                process.add(child)
        else:
            tree.score = max([(-1 * x.score) for x in tree.children] + [-1])

    scores_possible_moves = [(-1 * x.score) for x in state.children]
    index = scores_possible_moves.index(max(scores_possible_moves))
    game.current_state = old_state
    return old_state.get_possible_moves()[index]


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
