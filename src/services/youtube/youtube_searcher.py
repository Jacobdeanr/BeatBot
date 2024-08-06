from youtube_search import YoutubeSearch

class YouTubeSearcher:
    def __init__(self):
        pass
    
    def perform_search(self, query: str, limit=1) -> str:
        #print(f"YoutubeSearch for {query}")
        try:
            results = YoutubeSearch(query, max_results=limit).to_dict()

            if len(results) == 0:
                return None

            #url = f"https://www.youtube.com{results[0]['url_suffix']}"
            return results
        except Exception as e:
            print(f"\tGeneral exception occurred during YouTubeSearcher.perform_search: {e}")
            return None
