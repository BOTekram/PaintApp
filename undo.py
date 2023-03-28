from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        self.stack = ArrayStack(10000)
        self.undo_stack = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        self.stack.push(action)
        self.undo_stack.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.stack.is_empty():
            return None

        action = self.stack.pop()
        self.undo_stack.push(action)
        action.undo_apply(grid)
        return action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.undo_stack.is_empty():
            return None

        action = self.undo_stack.pop()
        self.stack.push(action)
        action.redo_apply(grid)
        return action
