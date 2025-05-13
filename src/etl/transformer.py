import logging.config
import pandas as pd
import numpy as np
import logging
import yaml

# Load logging configuration
with open("src/config/logging.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class PokemonTransformer:
    def __init__(self):
        pass

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the raw pokemon data.

        Args:
        df (pd.DataFrame): The raw DataFrame containing pokemon data.

        Returns:
        pd.DataFrame: The transformed DataFrame.
        """

        try:
            # Basic data cleaning
            df = self._rename_columns(df)
            df = self._handle_missing_values(df)
            df = self._convert_data_types(df)
            df = self._add_region_column(df)
            df = self._calculate_total_stats(df)

            # Feature engineering
            df = self._create_evolution_flags(df)

            logger.info("Data transformation completed successfully.")
            return df

        except Exception as e:
            logger.error(f"An error occured during data transformation: {str(e)}")
            return None

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Renames columns for consistency."""
        column_mapping = {
            "#": "id",
            "Name": "name",
            "Type 1": "type1",
            "Type 2": "type2",
            "Total": "total",
            "HP": "hp",
            "Attack": "attack",
            "Defense": "defense",
            "Sp. Atk": "sp_atk",
            "Sp. Def": "sp_def",
            "Speed": "speed",
            "Generation": "generation",
            "Legendary": "is_legendary",
        }
        df = df.rename(columns=column_mapping)
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handles missing values in the DataFrame."""
        if "type2" in df.columns:
            df["type2"] = df["type2"].fillna("unknown")
        return df

    def _convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Converts data types for consistency."""
        if "is_legendary" in df.columns:
            df["is_legendary"] = df["is_legendary"].astype(bool)
        return df

    def _add_region_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds region column based on the generation."""
        # Define region mappping based on generation
        region_mapping = {
            1: "Kanto",
            2: "Johto",
            3: "Hoenn",
            4: "Sinnoh",
            5: "Unova",
            6: "Kalos",
        }
        if "generation" in df.columns:
            df["region"] = df["generation"].map(region_mapping)
        return df

    def _create_evolution_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Creates flags to indicate if a Pokemon can evolve."""
        # This is a placeholder; actual implementation depends on evolution data
        df["can_evolve"] = True  # Assume all can evolve for now
        return df

    def _calculate_total_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculates the total stats for each Pokemon."""
        # Ensure stats columns are numeric
        stats_columns = ["hp", "attack", "defense", "sp_atk", "sp_def", "speed"]
        for col in stats_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Calculate total stats
        df["total"] = df[stats_columns].sum(axis=1)
        return df
