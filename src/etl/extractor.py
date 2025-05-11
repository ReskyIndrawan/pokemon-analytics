import logging.config
import pandas as pd
import logging
import yaml

# Load logging configuration
with open("src/config/logging.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class PokemonExtractor:
    def __init__(self, data_path: str = "data/raw/pokemon.csv"):
        """
        Intializes the PokemonExtractor with the path to the CSV file.

        Args:
        data_path (str): The path to the pokemon.csv file.
        """
        self.data_path = data_path

    def extract(self) -> pd.DataFrame:
        """
        Extracts the pokemon data from the CSV file.

        Returns:
        pd.DataFrame: A DataFrame containing the pokemon data, or None if an error occurs.
        """

        try:
            df = pd.read_csv(self.data_path)
            logger.info(f"Successfully extracted data from {self.data_path}")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None


if __name__ == "__main__":
    extractor = PokemonExtractor()
    data = extractor.extract()

    if data is not None:
        print(data.head())
    else:
        print("Failed to extract data.")
