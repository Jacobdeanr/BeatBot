import re

class YouTubeURL:
    def __init__(self):
        pass

    youtube_url_pattern = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    def is_youtube_url(self, query) -> bool:
        match = self.youtube_url_pattern.match(query)
        #print(f'\t{query} = {match}')
        return bool(match)

    def is_playlist_url(self, url) -> bool:
        return "list=" in url