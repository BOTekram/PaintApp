from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import *
from typing import Tuple
from data_structures.referential_array import ArrayR
from data_structures.stack_adt import *
from layers import *
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self) -> None:
        '''
        Initialize SetLayerStore

        Time complexity: O(1) Constant Time Complexity
        '''
        self._l = ArrayR(1)
        self._inv = False

    def add(self, layer: Layer) -> bool:
        '''
        Adding a layer to the store by replacing any existing layer.
        If the LayerStore was changed, Returns true.

        :param layer: layer that is to be added
        :return: True if layerStore was changed, otherwise False

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): when layer to be added is already present in the store
        Worst Case: Same as best case as replacing a layer is constant time regardless of input
        '''
        if self._l[0] == layer:
            return False
        self._l[0] = layer
        return True

    def get_color(self, start, timestamp, x, y) -> Tuple[int, int, int]:
        '''
        Given the current layer, Returns the colour this layer should show.

        :param start: Initial color
        :param timestamp: Current timestamp
        :param x: x-coordinate of point
        :param y: y-coordinate of point
        :return: After applying current layer in store, the resulting color

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): If all layers are absent in store, returns start color
        Worst Case: Same as best case as applying layer or returning start color are both O(1) Constant Time
        '''
        if not self._l[0]:
            if self._inv:
                return invert.apply(start, timestamp, x, y)
            return start
        else:
            start = self._l[0].apply(start, timestamp, x, y)
        if self._inv:
            return invert.apply(start, timestamp, x, y)
        return start

    def erase(self, layer: Layer) -> bool:
        '''
        Removes single layer.
        Ignore that is selected currently.
        If LayerStore was actually changed, Returns true.

        :param layer: Layer that is to be removed
        :return: True if layerStore was changed, otherwise return False

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): When all layers are absent in store, returns False
        Worst CAse: O(1): Same as best case as removing layer is constant time

        '''
        if not self._l[0]:
            return False
        self._l[0] = None
        return True

    def special(self):
        '''
        Special mode.
        Inverts the color output.

        :return: None

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): As it only flips a boolean value
        Worst Case: Same as best case
        '''
        self._inv = not self._inv
    

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    
    def __init__(self) -> None:
        '''
        Initialize AdditiveLayerStore

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1): Method initializes layer queue with fixed size
        Worst Case: O(1): Same as best case as it due to having just one operation
    
        '''
        self._layers = CircularQueue(100*20)
        

    def add(self, layer: Layer) -> bool:
        '''
        To the last layer, add a new layer.
        Return False if the store if full.
        Returns True if the LayerStore was changed

        :param layer: Layer that is to be added.
        :return: True if the addition is successful,Otherwise Return False.

        Time Complexity: O(log(n)), where n is the number of layers
        Best Case: O(1): If layer is present in the store already
        Worst Case: O(log(n)): If layer is absent in store, and binary search is needed to trace the new position of the layer is sorted list.
        
        '''
        if self._layers.is_full():
            return False
        else:
            self._layers.append(layer)
            return True
        

    def get_color(self, start, timestamp, x, y) -> Tuple[int, int, int]:
        '''
        Aftering applying all the layers in store, returns the resulting colour 

        :param start: The initial color.
        :param timestamp: The current timestamp.
        :param x: x-coordinate of the point.
        :param y: y-coordinate of the point.
        :return: The resulting color after applying all the layers in the store.

        Time Complexity: O(N) (Linear Time Complexity)
        Best Case: O(1) Constant Time Complexity: The method simply returns the start color if the store is empty.
        Worst Case: O(N) Linear Time Complexity: The method loops through all the layers in the queue and applies them in order.

        '''

        
        new_queue = CircularQueue(100*20)
        output = start
        if self._layers.is_empty():
            return start
        else:
            for _ in range(len(self._layers)):
                curr_layer = self._layers.serve()
                new_queue.append(curr_layer)
                output = curr_layer.apply(output, timestamp,x,y)
            self._layers = new_queue
            return output
        

    def erase(self, layer: Layer) -> bool:
        '''
        Removes the layer that was first added.
        If store is empty, returns False
        
        :param layer: Layer that is to be removed.
        :return: return True if removal successful, or else return False.

        Time Complexity: O(1) Constant Time Complexity
        Best Case: O(1) Constant Time Complexity: Removes first layer from the queue
        Worst Case: O(1) Constant Time Complexity: Same to best case as it has one operation
        '''
        if not self._layers.is_empty():
            self._layers.serve()
            return True
        return False
        

    def special(self):
        '''
        Simply reverses the order of the present layers. i.e first becomes last, last becomes first.

        Time Complexity: O(N) Linear Time Complexity.
        Best Case: O(1) Constant Time Complexity: Applicable when one layer is present in store only.
        Worst Case: O(N) Linear Time Complexity: Applicable when N layers are present in store.
        '''
        size = len(self._layers)
        temp_stack = ArrayStack(size)
        for _ in range(size):
            temp_stack.push(self._layers.serve())
        while not temp_stack.is_empty():
            self._layers.append(temp_stack.pop())
        


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        '''
        Initializes all the necessary attributes for SequenceLayerStore

        Time Complexity: O(1) Constant time complexity
        Best Case: O(1)
        Worst Case: Same as best case
        '''
        self._layers = ArraySortedList(100*20)
        self._layers_lex = ArraySortedList(100*20)

    def add(self, layer: Layer) -> bool:
        """
       Adds a layer to the store and makes sure it is applied.
       Returns True if LayerStore was changed.
       Returns False if not.

       Time Complexity: O(log(n)), n is the number of layers in store
       Best Case: O(1): if layer already present in store
       Worst Case: O(log(n)): If layer is absent in store, and binary search is needed to trace the new position of the layer is sorted list.
        """
        if not self._layers.is_full():
            item = ListItem(layer, layer.index)
            item_lex = ListItem(layer, layer.name)
            if item in self._layers:
                return False
            else:
                self._layers.add(item)
                self._layers_lex.add(item_lex)
                return True
            
        return False
        

    def get_color(self, start, timestamp, x, y) -> Tuple[int, int, int]:
       '''
        After applying all currently applied layers to it,
        Returns the color of the grid at the given (x,y) position.

        Time Complexity: O(n), where n is the number of layers currently applied to the grid.
        Best Case: O(1) if there are no layers currently applied to the grid.
        Worst Case: O(n) if all layers currently applied to the grid need to be applied to the given (x,y) position.
    
       '''
       output = start
       if self._layers.is_empty():
           return output
       else:
            for idx in range(len(self._layers)):
                curr_layer = self._layers[idx].value
                output  =  curr_layer.apply(output,timestamp, x, y)
            return output
           
        

    def erase(self, layer: Layer) -> bool:
        '''
        Makes sure the given layer type isn't applied in the store.
        If LayerStore was changed, Returns True

        Time Complexity: O(log(n)) Logarithmic Time
        Best Case: O(1): Only if layer is absent in the store
        Worst Case: O(log(n)):If Layer is present in the store, and binary search is needed in ArraySortedList to find the correct position on the layer
        '''
        item = ListItem(layer,layer.index)
        if item in self._layers:
            self._layers.remove(item)
            item.key = item.value.name  
            self._layers_lex.remove(item)
            return True
        else:
            return False

    def special(self) -> bool:
            '''
            Removes layer with median name value from all the currently applied layers in the layerstore.
            For the event of two layers as median names, pick the lexicographically one
            Returns True if layer was changed actually

            Time Complexity: O(log(n)), where n is the number of layers in store.
            Best Case: O(1): Only if the store is empty.
            Worst Case: O(log(n)): if binary search is used to find the median layer
            '''
            if self._layers_lex.is_empty():
                return False
            

            if len(self._layers)%2==1:
                median_index = (len(self._layers)-1)//2
                item = self._layers_lex[median_index] 
            elif len(self._layers)%2==0:
                second_median_index = (len(self._layers)//2) 
                first_median_index = second_median_index - 1
                first_item = self._layers_lex[first_median_index]
                second_item = self._layers_lex[second_median_index]

                if first_item.key > second_item.key:
                    item = second_item

                else:
                    item = first_item
            
            self._layers_lex.remove(item)
            item.key = item.value.index
            self._layers.remove(item)
            return True
    



    