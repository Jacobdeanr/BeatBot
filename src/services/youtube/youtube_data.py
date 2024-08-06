import datetime
#from download_utils.audio_download_manager import AudioDownloadManager
from pytubefix import YouTube, Playlist, Channel, Stream

class YouTubeData:
    def __init__(self):
        pass
              
    def get_playlist(self, url: str): 
        return Playlist(url)
        
    def get_audio_stream(self, yt: YouTube):
        try:            
            stream = yt.streams.filter(only_audio=True).first()
            if stream:
                return stream
            return None
        except Exception as e:
            #print(f"Error fetching audio stream: {e}")
            return None
        
    def get_youtube_object(self, url: str):
        return YouTube(url)

    def get_video_information(self, url: str):
        try:
            yt = YouTube(url)
        except Exception as e:
            print(f"Error fetching video information: {e}")
            return None

        return yt
    
    #Deprecated
    def get_local_file(self, stem: str):
        return None
    
    def format_publish_date(self, publish_date) -> str:
        if publish_date:
            return datetime.datetime.strftime(publish_date, "%m/%d/%Y")
        return "Unknown"


def main():
    #Need to determine if age restricted.
    #example: https://www.youtube.com/watch?v=wiRRsHPTSC8

    age_restricted_video = YouTube(url='https://www.youtube.com/watch?v=wiRRsHPTSC8')
    print(age_restricted_video.age_restricted)

    # Non Age Blocked:
    # https://www.youtube.com/watch?v=ogodJg67Y4M

    url = 'https://www.youtube.com/watch?v=ogodJg67Y4M'
    ytd = YouTubeData()
    vid_info = ytd.get_video_information(url=url)
    print(vid_info)

if __name__ == "__main__":
    main()