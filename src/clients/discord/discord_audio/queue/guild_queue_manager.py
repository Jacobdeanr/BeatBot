from threading import Lock
from typing import Optional, Dict
from clients.discord.discord_audio.queue.guild_queue import GuildQueue
from clients.discord.discord_audio.queue.queue_item import QueueItem

class GuildQueueManager():
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.song_queues = {}
        return cls._instance

    def get_guild_queue_by_id(self, guild_id: int) -> GuildQueue:
        """Ensure a guild queue exists for the given guild_id, or creates one."""
        return self.song_queues.setdefault(guild_id, GuildQueue())

    def pop_item_from_guild_queue_by_id(self, guild_id: int, index: int) -> QueueItem:
        """Remove and return an item by index from the guild's queue."""
        return self.song_queues[guild_id].pop_item(index)
    
    def add_item_to_guild_queue_by_id_end(self, guild_id: int, item: QueueItem) -> None:
        """Add an item to the guild's queue at the specified position."""
        self.song_queues[guild_id].add_item_to_end(item)

    def clear_guild_queue_by_id(self, guild_id: int) -> None:
        """Clear the guild's queue if it is not empty."""
        if len(self.song_queues[guild_id].queue) > 0:
            self.song_queues[guild_id].clear_queue()

    def set_current_song_by_id(self, guild_id: int, item: dict) -> None:
        """Set the current song for a guild based on item."""
        self.song_queues[guild_id].set_current_song(item)

    def get_current_song_by_id(self, guild_id: int):
        """Retrieve the current song for a guild."""
        return self.song_queues[guild_id].get_current_song()