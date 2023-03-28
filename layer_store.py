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
        '''
        self._l = ArrayR(1)
        self._inv = False

    def add(self, layer: Layer) -> bool:
        '''
        Adding a layer to the store by replacing any existing layer.
        If the LayerStore was changed, Returns true.
        '''
        if self._l[0] == layer:
            return False
        self._l[0] = layer
        return True

    def get_color(self, start, timestamp, x, y) -> Tuple[int, int, int]:
        '''
        Given the current layer, Returns the colour this layer should show.
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
        '''
        if not self._l[0]:
            return False
        self._l[0] = None
        return True

    def special(self):
        '''
        Special mode.
        Inverts the color output.
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
        self._layers = CircularQueue(100*20)
        

    def add(self, layer: Layer) -> bool:
        if self._layers.is_full():
            return False
        else:
            self._layers.append(layer)
            return True
        

    def get_color(self, start, timestamp, x, y) -> Tuple[int, int, int]:
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
        if not self._layers.is_empty():
            self._layers.serve()
            return True
        return False
        

    def special(self):

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
        self._layers = ArraySortedList(100*20)
        self._layers_lex = ArraySortedList(100*20)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store and ensure it's applied.
        Returns true if the LayerStore was actually changed.
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
       output = start
       if self._layers.is_empty():
           return output
       else:
            for idx in range(len(self._layers)):
                curr_layer = self._layers[idx].value
                output  =  curr_layer.apply(output,timestamp, x, y)
            return output
           
        

    def erase(self, layer: Layer) -> bool:
        item = ListItem(layer,layer.index)
        if item in self._layers:
            self._layers.remove(item)
            item.key = item.value.name  
            self._layers_lex.remove(item)
            return True
        else:
            return False

    def special(self):
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
    