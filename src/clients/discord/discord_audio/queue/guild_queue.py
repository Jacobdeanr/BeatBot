from typing import Any, Optional


class GuildQueue:
    def __init__(self):
        self.queue:list = []
        self.current_song = None

    def __str__(self):
        queue_str = "\n ".join(str(song) for song in self.queue)
        return f'\nSong Queue: {queue_str}'

    def add_item_to_end(self, item) -> None:
        """
        Add an item to the end of the queue.

        Parameters:
            item: The item to be added to the queue.

        Return:
            None
        """
        self.queue.append(item)

    def place_item(self, item, position: int) -> None:
        """
        Add an item to the queue at the specified position.

        Parameters:
            item (any): The item to add to the queue.
            position (int, optional): The position in the queue to add the item to. Defaults to None.

        Raises:
            ValueError: If the position is out of range for the queue.
        """
        try:
            self.queue.insert(position, item)
        except IndexError as e:
            raise ValueError(f'Position {position} is out of range for queue with length {len(self.queue)}') from e

    def pop_item(self, index: int) -> Optional[Any]:
        """
        Remove and return an item from the queue at the specified index.

        Parameters:
            index (int): The index of the item to retrieve.

        Returns:
            The item at the specified index if it exists, otherwise None.

        Raises:
            IndexError: If the index is out of range for the queue.
        """
        try:
            return self.queue.pop(index)
        except IndexError as e:
            raise IndexError(f'Index {index} is out of range for queue with length {len(self.queue)}') from e

    
    def clear_queue(self) -> None: 
        self.queue = []
    
    def is_empty(self) -> bool:
        if len(self.queue) > 0:
            return False
        else:
            return True
        
    def set_current_song(self, item):
        """
        Set the current song to the given item.
        
        Parameters:
            self (object): The object instance
            item (any): The item to set as the current song
        Returns:
            None
        """
        self.current_song = item

    def get_current_song(self) -> Optional[Any]:
        """
        Return the current song if it is set, otherwise return None.

        Returns:
            The current song if it is set, otherwise None.
        """
        return self.current_song
