from ..message_utilities import EmbedUtilities
from pytubefix import YouTube

class SpotifyEmbedCreator():
    _instance = None
    @staticmethod
    def create_album_embed(album):
        track_strings = []
        for track in album.tracks.items:
            track_strings.append(f"{track.track_number}: {track.name}")

        fields = [
            ("Artist", album.artists[0].name, True),
            ("Release Date", album.release_date, True),
            ("Total Tracks", album.total_tracks, True),
            ("Tracks", "\n".join(track_strings), False)
        ]

        return EmbedUtilities.create_embed(
            title=f"{album.name}",
            color=0xb526d9,
            url=album.external_urls,
            image_url=album.images[1].url,
            fields=fields
        )
    
    @staticmethod
    def create_artist_embed(artist, top_songs:list):
        
        top_tracks = []
        for track in top_songs:
            top_tracks.append(f'{track.artists[0].name} - {track.name}')

        fields = [
            ("Followers", f"{artist.followers:,}", False),
            ("Popularity", f"{artist.popularity} - {SpotifyEmbedCreator._get_popularity_name(artist.popularity)}", True),
            ("Genres", ", ".join(artist.genres), True),
            ("Top Tracks", "\n".join(top_tracks), False)
        ]

        return EmbedUtilities.create_embed(
            title=f"{artist.name}",
            color=0xb526d9,
            url=artist.external_urls,
            image_url=artist.images[0].url,
            fields=fields
        )
   
    @staticmethod
    def create_playlist_embed(playlist):
        # Elipses after MAX_DISPLAY
        MAX_DISPLAY = 10
        num_tracks_to_display = min(playlist.tracks.total, MAX_DISPLAY)
        track_strings = [f"{items.track.artists[0].name} - {items.track.name}" for items in playlist.tracks.items[:num_tracks_to_display]]
        if playlist.tracks.total > MAX_DISPLAY:
            track_strings.append("...")

        fields = [
            ("Tracks", "\n".join(track_strings), False),
            ("Total Tracks", playlist.tracks.total, True),
            ("Followers", f"{playlist.followers:,}", True),
        ]

        return EmbedUtilities.create_embed(
            title=f"{playlist.name}",
            color=0xb526d9,
            url=playlist.external_urls,
            image_url=playlist.images[0].url,
            fields=fields
        )
    
    @staticmethod
    def create_track_embed(track):
        track_artist = track.artists[0]
        album = track.album

        # Calculate the duration of the track.
        con_sec, con_min, con_hour = EmbedUtilities.convertMillis(int(track.duration_ms))
        duration_value = f"{con_hour:02d}:{con_min:02d}:{con_sec:02d}" if con_hour != 00 else f"{con_min:02d}:{con_sec:02d}"

        fields = [
            ("Album", album.name, True),
            ("Duration", duration_value, True),
            ("Track Number", track.track_number, True),
            ("Popularity", f"{track.popularity} - {SpotifyEmbedCreator._get_popularity_name(track.popularity)}", True),
            ("Artists", "\n".join([artist.name for artist in track.artists]), True)
        ]

        return EmbedUtilities.create_embed(
            title=f"{track_artist.name} - {track.name}",
            color=0xb526d9,
            url=track.external_urls,
            image_url=album.images[1].url,
            fields=fields
        )
    
    @staticmethod
    def create_song_search_embed(search_result_urls:list):
        fields = []
        for i, track in enumerate(search_result_urls):
            if(track.explicit):
                field_title = f"{i+1}. (Explicit) {track.name} - {track.artists[0].name}"
            else:
                field_title = f"{i+1}. {track.name} - {track.artists[0].name}"
            
            con_sec, con_min, con_hour = EmbedUtilities.convertMillis(int(track.duration_ms))
            duration_value = f"{con_hour:02d}:{con_min:02d}:{con_sec:02d}" if con_hour != 00 else f"{con_min:02d}:{con_sec:02d}"

            fields.append((field_title, f"Album: {track.album.name}\nDuration: {duration_value}\nLink: {track.external_urls}", False))

        return EmbedUtilities.create_embed(
            title=f"Results",
            color=0xb526d9,
            description="Please select which result you would like to use",
            fields=fields
        )

    @staticmethod
    def _get_popularity_name(score) -> str:
        if 0 <= score <= 2:
            return "Ghost Town"
        elif 3 <= score <= 5:
            return "Hidden Gem"
        elif 6 <= score <= 10:
            return "Under the Radar"
        elif 11 <= score <= 15:
            return "Whisper in the Wind"
        elif 16 <= score <= 20:
            return "Buzz Builder"
        elif 21 <= score <= 30:
            return "On the Up and Up"
        elif 31 <= score <= 35:
            return "Crowd Pleaser"
        elif 36 <= score <= 40:
            return "Talk of the Town"
        elif 41 <= score <= 50:
            return "Trendsetter"
        elif 51 <= score <= 55:
            return "Hot Topic"
        elif 56 <= score <= 60:
            return "People’s Choice"
        elif 61 <= score <= 70:
            return "Chart Climber"
        elif 71 <= score <= 75:
            return "Viral Sensation"
        elif 76 <= score <= 80:
            return "Cultural Phenomenon"
        elif 81 <= score <= 85:
            return "Icon in the Making"
        elif 86 <= score <= 90:
            return "Hall of Fame"
        elif 91 <= score <= 95:
            return "Mythic Status"
        elif 96 <= score <= 100:
            return "Universal Acclaim"
        else:
            return str(score)
        
class YoutubeEmbedCreator():
    _instance = None
    
    @staticmethod
    def create_playlist_embed(playlist):
        # Elipses after MAX_DISPLAY
        MAX_DISPLAY = 10
        
        #extract the videos from playlist.. This generates a list of YouTube Objects.
        # We only need the ID
        # Only do this up to the MAX_DISPLAY
        videos:list = playlist.videos
        
        #Sometimes there are no views? Idk I don't have time to look into it
        try:
            tertiary_field = ("Views", playlist.views, True)
        except Exception as e:
            tertiary_field = ("Description", playlist.description, True)

        num_tracks_to_display = min(len(videos), MAX_DISPLAY)
        track_strings = [f"{video.author} - {video.title}" for video in videos[:num_tracks_to_display]]
        
        if len(videos) > MAX_DISPLAY:
            track_strings.append("...")

        fields = [
            ("Tracks", "\n".join(track_strings), False),
            ("Total Tracks", len(videos), True),
            tertiary_field,
        ]

        return EmbedUtilities.create_embed(
            title=playlist.title,
            color=0xb526d9,
            url=playlist.playlist_url,
            image_url=videos[0].thumbnail_url,
            fields=fields
        )

    @staticmethod
    def create_video_embed(video: YouTube):
        try:
            # Calculate the duration of the track.
            con_sec, con_min, con_hour = EmbedUtilities.convertMillis(int(video.length*1000))
            duration_value = f"{con_hour:02d}:{con_min:02d}:{con_sec:02d}" if con_hour != 00 else f"{con_min:02d}:{con_sec:02d}"

            fields = [
                ("Title", video.title, True),
                ("Duration", duration_value, True),
                ("Popularity", video.views, True),
                ("Uploader", video.author, True)
            ]

            return EmbedUtilities.create_embed(
                title=video.title,
                color=0xb526d9,
                url=video.watch_url,
                image_url=video.thumbnail_url,
                fields=fields
            )
        except Exception as e:
            print(f"Error creating video embed: {e}")

    @staticmethod
    def create_video_search_embed(search_result_urls:list):
        fields = []
        for i, video in enumerate(search_result_urls):
            field_title = f"{i+1}. {video.author} - {video.title}"
            
            con_sec, con_min, con_hour = EmbedUtilities.convertMillis(int(video.length*1000))
            duration_value = f"{con_hour:02d}:{con_min:02d}:{con_sec:02d}" if con_hour != 00 else f"{con_min:02d}:{con_sec:02d}"

            fields.append((field_title, f"Views: {video.views}\nDuration: {duration_value}\nLink: {video.watch_url}", False))

        return EmbedUtilities.create_embed(
            title=f"Results",
            color=0xb526d9,
            description="Please select which result you would like to use",
            fields=fields
        )
