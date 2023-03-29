from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import *


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Time Complexity: O(n) Linear Time Complexity respect to product of x and y dimension
        Best Case: O(1) Constant Time: Considering when x and y is 1 which is the smallest possible grid
        Worst Case: O(n) Linear Time: When x and y at maximum values
        """
        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE
        self.grid = ArrayR(x)


        for i in range(self.x):
            row = ArrayR(self.y)
            for j in range(self.y):
                if draw_style == Grid.DRAW_STYLE_SET:
                    row[j] = SetLayerStore()
                elif draw_style == Grid.DRAW_STYLE_ADD:
                    row[j] = AdditiveLayerStore()
                elif draw_style == Grid.DRAW_STYLE_SEQUENCE:
                    row[j] = SequenceLayerStore()
            self.grid[i] = row

    def __getitem__(self, index: int) -> ArrayR:
        '''
        Get the row at the indicated index in grid
        
        Time Complexity: O(1) Constant Time Complexity
        '''
        return self.grid[index]


    def increase_brush_size(self) -> None:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Time Complexity: O(1) (Constant Time)
        Best Case: O(1) (Constant Time): The method checks and updates the brush size only, so it takes constant time
        Worst Case: O(1) (Constant Time)e: Same as best case as it only has one operation
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size +=1

    def decrease_brush_size(self) -> None:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Time Complexity: O(1) (Constant Time)
        Best Case: O(1) Contant Time Complexity: The method checks and updates the brush size only, so it takes constant time
        Worst Case: O(1) Constant Time Complexity: Same as best case as it only has one operation
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -=1

    def special(self) -> None:
        """
        Activate the special affect on all grid squares.

        Time Complexity: O(N) Linear Time Complexity
        Best Case: O(1) Constant Time Complexity: if both x and y are 1.
        Worst Case: O(N) Linear Time Complexity: when both x and y have the maximum allowed values.
        """
        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()


    def manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        Calculation of the Manhattan distance in between the two points (x1, y1) and (x2, y2).

        :param x1: first point x-coordinate.
        :param y1: first point y-coordinate.
        :param x2: second point x-coordinate.
        :param y2: second point y-coordinate.
        :return: Two points Manhattan Distance.

        Time Complexity: O(1) (Constant Time Complexity)
        Best Case: O(1) Constant Time Complexity: due to invlovement of simple arithmatic equations
        Worst Case: O(1) Constant Time Complexity: due to constant complexity
        """
        return abs(x1 - x2) + abs(y1 - y2)

    def on_paint(self, layer: Layer, px: int, py: int) -> None:
        """
        Paints all grid squares within a specified Manhattan distance
        based on the current brush size.

        :param layer: Layer object to paint with.
        :param px: x-coordinate of the painting point.
        :param py: y-coordinate of the painting point.

        Time Complexity: O(N^2) Qudratic Time Complexity:considering N to be maximum of x and y.
        Best Case: O(1) Constant Time Complexity: when x and y is 1.
        Worst Case: O(N^2) Qudratic Time Complexity: when both x and y have the maximum allowed values.

        """
        for i in range(self.x):
            for j in range(self.y):
                if self.manhattan_distance(px, py, i, j) <= self.brush_size:
                    self.grid[i][j].add(layer)
  
