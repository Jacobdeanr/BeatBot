from ..services_utils.audio_service import AudioService
from .youtube_data import YouTubeData
from .youtube_url import YouTubeURL
from .youtube_searcher import YouTubeSearcher

#typing
#from typing import TYPE_CHECKING
#if TYPE_CHECKING:
from pytubefix import YouTube, Playlist, Channel, Stream

class YouTubeService(AudioService):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.search_handler = YouTubeSearcher()
        self.data_handler = YouTubeData()
        self.url_validator = YouTubeURL()

    def __str__(self):
        return "YouTube Service"

    def __repr__(self):
        return "YouTube Service"

    def perform_search(self, query: str, limit=4) -> list[dict]:
        return self.search_handler.perform_search(query, limit)
    
    def search_and_bind(self, query: str, limit=1) -> list[YouTube]:
        search_results: list[dict] = self.search_handler.perform_search(query, limit)
        if search_results is None:
            return None

        answer = []
        for video in search_results:
            if video is None:
                return None
            
            item:YouTube = self.get_youtube_by_url(f"https://www.youtube.com{video['url_suffix']}")
            if item is None:
                return None
            answer.append(item)

        return answer
           
    def download_song(self, url: str, id: str) -> str:
        pass
    
    def get_youtube_by_url(self, url: str) -> YouTube:
        return self.data_handler.get_video_information(url)
    
    def get_playlist_from_url(self, url: str) -> Playlist:
        return self.data_handler.get_playlist(url)
    
    def get_audio_stream(self, yt:YouTube) -> Stream:
        #if yt.age_restricted:
        #    return None
        #print(yt.age_restricted)
        results = self.data_handler.get_audio_stream(yt)
        if results is not None:
            return results.url
        return None
    
    def get_playback_stream_from_str(self, item: str):
        response:list[YouTube] = self.search_and_bind(item, 1)
        item:YouTube = response[0]
        if item is None:
            return None
        
        #HACK
        #Should we be doing this here?
        if item.age_restricted:
            return None
        
        #print(item.watch_url)
            
        return self.get_audio_stream(item)