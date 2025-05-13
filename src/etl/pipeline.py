from src.etl.extractor import PokemonExtractor
from src.etl.transformer import PokemonTransformer
import logging
import yaml

# Load logging configuration
with open("src/config/logging.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def run():
    """
    Runs the ETL pipeline for Pokemon data.
    """
    extractor = PokemonExtractor()
    transformer = PokemonTransformer()

    logger.info("Starting ETL process for Pokemon data")
    raw_data = extractor.extract()

    if raw_data is not None:
        transformed_data = transformer.transform(raw_data)

        if transformed_data is not None:
            # Save the transformed data to a CSV file
            file_path = "data/processed/pokemon_transformed.csv"
            transformed_data.to_csv(file_path, index=False)
            logger.info(f"Transformed data saved to {file_path}")
        else:
            logger.error("Transformation failed for Pokemon data")
    else:
        logger.error("Extraction failed for Pokemon data")


if __name__ == "__main__":
    run()
