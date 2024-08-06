from services.youtube.youtube_service import YouTubeService
from services.spotify.spotify_service import SpotifyService
import sys
sys.path.append("...")

from clients.discord.discord_integrations.youtube import YoutubeIntegration
from clients.discord.discord_integrations.spotify import SpotifyIntegration

class ServiceFactory:
    def __init__(self):
        self.services = {
            "youtube": YouTubeService(),
            "youtu.be": YouTubeService(),
            "spotify": SpotifyService(),
            # "vimeo.com": VimeoService(),
            # "soundcloud.com": SoundCloudService()
        }
        self.default_service = YouTubeService()  # Set a default service

    #def get_service(self, url: str):
    #    for domain, service in self.services.items():
    #        if domain in url:
    #            return service
    #    #return self.default_service
    #    return None
    
    def get_service(self, url: str):
        for domain, service in self.services.items():
            if domain in url:
                if isinstance(service, YouTubeService):
                    return YoutubeIntegration(service)
                elif isinstance(service, SpotifyService):
                    return SpotifyIntegration(service)

        # return self.default_service
        return None