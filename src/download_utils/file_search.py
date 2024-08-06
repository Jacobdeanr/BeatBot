import os
import glob

class FileSearch:

    @staticmethod
    def find_existing_file(path, stem):
        """
        Searches for an existing downloaded file with the given video ID.

        :param video_id: The YouTube video ID to search for
        :return: Path to the existing file if found, None otherwise
        """
        pattern = os.path.join(path, f"{stem}.*")
        files = glob.glob(pattern)
        return files[0] if files else None