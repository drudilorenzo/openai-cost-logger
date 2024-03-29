from pathlib import Path

"""OpenAI cost tracker utilities functions."""
class OpenAICostTrackerUtils:

    @staticmethod
    def get_api_key(path: str) -> str:
        """Return the key contained in the file.

        Args:
            path: path to file.

        Returns:
            The key contained in the file.
        """
        with open(Path(path), "r") as f:
            return f.read()