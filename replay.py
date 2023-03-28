from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import Queue
from data_structures.array_sorted_list import *

# class ReplayTracker:


#     def start_replay(self) -> None:
#         """
#         Called whenever we should stop taking actions, and start playing them back.

#         Useful if you have any setup to do before `play_next_action` should be called.
#         """
#         pass

        
#     def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
#         """
#         Adds an action to the replay.

#         `is_undo` specifies whether the action was an undo action or not.
#         Special, Redo, and Draw all have this is False.
#         """
#         pass

#     def play_next_action(self, grid: Grid) -> bool:
#         """
#         Plays the next replay action on the grid.
#         Returns a boolean.
#             - If there were no more actions to play, and so nothing happened, return True.
#             - Otherwise, return False.
#         """
#         pass



class ReplayTracker:
    def __init__(self) -> None:
        self.actions: Queue[PaintAction] = Queue()
        self.replay_started = False

    def start_replay(self) -> None:
        self.replay_started = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        if not self.replay_started:
            self.actions.enqueue(action)

    def play_next_action(self, grid: Grid) -> bool:
        if not self.actions.is_empty():
            action = self.actions.dequeue()
            action.apply(grid)
            return False
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

