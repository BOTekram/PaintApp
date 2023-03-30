from __future__ import annotations
from action import PaintAction, PaintStep
from grid import Grid
from data_structures.stack_adt import ArrayStack
from undo import UndoTracker
from data_structures.queue_adt import CircularQueue

from layers import green, red, blue

class ReplayTracker:


    def __init__(self, max_capacity: int = 10000) -> None:
        '''
        Initializes instance of ReplayTracker class using CircularQueue to store actions and UndoTracker

        Time Complexity: O(1) Constant Time Complexity
        '''

        self.actions: CircularQueue = CircularQueue(max_capacity)
        self.undo= UndoTracker()
        self.is_replaying = False

    def start_replay(self) -> None:
        """
         Called whenever we should stop taking actions, and start playing them back.

         Useful if you have any setup to do before `play_next_action` should be called.

         Time Complexity: O(1) Constant Time Complexity
         """
        self.is_replaying = True

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
         Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
         Special, Redo, and Draw all have this is False.

         Time Complexity: O(1) Constant Time Complexity
         Best Case: O(1): if actions CircularQueue is not full
         Worst Case: O(1): Same as best case , when CircularQueue is full and actions are not added 
         """
        if not self.is_replaying:
            if not self.actions.is_full():
                self.actions.append((action,is_undo))
            
            

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): When no actions to play anymore
        Worst Case: O(1): Same as best case , When action is to play
        """
        if not self.actions.is_empty():
            curr = self.actions.serve()
            action = curr[0]
            is_undo = curr[1]

            if is_undo is True:
                self.undo.undo(grid)
            elif is_undo is False:
                action.redo_apply(grid)
                self.undo.add_action(action)


            return False
        else:
            return True

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

