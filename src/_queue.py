#! /usr/bin/env python3

from abc import abstractmethod, ABCMeta
import heapq

class EmptyException(Exception):
    pass

class Queue(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        """constructor
        """
        pass

    @abstractmethod
    def put(self, item:"Comparable", value:int=None) -> None:
        """Puts a new element in the queue

        Args:
            item:   The item to be put in the queue
            value:  Optional. If != None, a value to be associated to
                    the item to be used for any reason (eg, a priority
                    queue)
        """
        pass

    @abstractmethod
    def get(self) -> "Comparable":
        """Returns the first element in the queue, removing it from the queue

        Raises:
            EmptyException: The queue was empty
        """
        pass

    @abstractmethod
    def is_in(self, item:"Comparable") -> bool:
        """Returns True iff item is in the queue
        """
        pass

    @abstractmethod
    def qsize(self) -> int:
        """Returns the size of the queue
        """
        pass

class FifoQueue(Queue):
    """Implementation of a Fifo queue
    """
    def __init__(self) -> None:
        """constructor
        """
        self.elements = []

    def put(self, item:"Comparable", value:int=None) -> None:
        """Puts a new element in the queue
        """
        self.elements.append(item)

    def get(self) -> "Comparable":
        """Returns the first element in the queue, removing it from the queue

        Raises:
            EmptyException: The queue was empty
        """
        if not self.elements:
            raise EmptyException
        retval = self.elements[0]
        self.elements = self.elements[1:]
        return retval

    def is_in(self, item:"Comparable") -> bool:
        """Returns True iff item is in the queue
        """
        return item in self.elements

    def qsize(self) -> int:
        """Returns the size of the queue
        """
        return len(self.elements)

    def __str__(self) -> None:
        return str(self.elements)


class PriorityQueue(metaclass=ABCMeta):
    """Implementation of a Priority queue

    The first item is to be considered the one with the
    lowest priority
    """

    def __init__(self) -> None:
        """constructor
        """
        self.elements = []
        self.counter = 0

    def put(self, item:"Comparable", value:int=None) -> None:
        """Puts a new element in the queue

        Args:
            item:   The item to be put in the queue
            value:  The priority of the item
        """
        heapq.heappush(self.elements, (value,self.counter,item))
        self.counter += 1

    def get(self) -> "Comparable":
        """Returns the first element in the queue, removing it from the queue

        Raises:
            EmptyException: The queue was empty
        """
        try:
            return (heapq.heappop(self.elements))[2]
        except IndexError:
            raise EmptyException

    def is_in(self, item:"Comparable") -> bool:
        """Returns True iff item is in the queue
        """
        for t in self.elements:
            if t[2] == item:
                return True
        else:
            return False

    def qsize(self) -> int:
        """Returns the size of the queue
        """
        return len(self.elements)

    def __str__(self) -> None:
        return str(self.elements)

if __name__ == '__main__':
    fq = FifoQueue()
    fq.put(5)
    fq.put(6)
    fq.put(3)
    print(fq)
    pq = PriorityQueue()
    pq.put("cane", 2)
    pq.put("gatto", 1)
    pq.put("alce", 3)
    pq.put("felice", 0)
    print(pq)
    print(pq.get())
    print(pq.get())
    print(pq.get())
    try:
        print(pq.get())
    except EmptyException:
        print("Queue empty")
