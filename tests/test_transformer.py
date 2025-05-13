import unittest
import pandas as pd
import numpy as np
from src.etl.transformer import PokemonTransformer


class TestPokemonTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = PokemonTransformer()
        self.data = pd.DataFrame(
            {
                "#": [1, 2],
                "Name": ["Bulbasaur", "Ivysaur"],
                "Type 1": ["Grass", "Grass"],
                "Type 2": [np.nan, "Poison"],
                "Total": [318, 405],
                "HP": [45, 60],
                "Attack": [49, 62],
                "Defense": [49, 63],
                "Sp. Atk": [65, 80],
                "Sp. Def": [65, 80],
                "Speed": [45, 60],
                "Generation": [1, 1],
                "Legendary": [False, False],
            }
        )
        # Data yang sudah di-rename kolomnya
        self.renamed_data = self.transformer._rename_columns(self.data.copy())

    def test_rename_columns(self):
        transformed_df = self.transformer._rename_columns(self.data.copy())
        expected_columns = [
            "id",
            "name",
            "type1",
            "type2",
            "total",
            "hp",
            "attack",
            "defense",
            "sp_atk",
            "sp_def",
            "speed",
            "generation",
            "is_legendary",
        ]
        self.assertEqual(list(transformed_df.columns), expected_columns)

    def test_handle_missing_values(self):
        # Gunakan data yang sudah di-rename
        transformed_df = self.transformer._handle_missing_values(
            self.renamed_data.copy()
        )
        self.assertFalse(transformed_df["type2"].isnull().any())
        self.assertEqual(transformed_df["type2"][0], "unknown")

    def test_convert_data_types(self):
        # Gunakan data yang sudah di-rename
        transformed_df = self.transformer._convert_data_types(self.renamed_data.copy())
        self.assertEqual(transformed_df["is_legendary"].dtype, bool)

    def test_add_region_column(self):
        # Gunakan data yang sudah di-rename
        transformed_df = self.transformer._add_region_column(self.renamed_data.copy())
        self.assertTrue("region" in transformed_df.columns)
        self.assertEqual(transformed_df["region"][0], "Kanto")

    def test_create_evolution_flags(self):
        # Gunakan data yang sudah di-rename
        transformed_df = self.transformer._create_evolution_flags(
            self.renamed_data.copy()
        )
        self.assertTrue("can_evolve" in transformed_df.columns)
        self.assertTrue(
            transformed_df["can_evolve"].dtype == bool
            or transformed_df["can_evolve"].dtype == np.bool_
        )

    def test_calculate_total_stats(self):
        # Gunakan data yang sudah di-rename
        transformed_df = self.transformer._calculate_total_stats(
            self.renamed_data.copy()
        )
        self.assertTrue("total" in transformed_df.columns)
        expected_total = (
            self.renamed_data["hp"][0]
            + self.renamed_data["attack"][0]
            + self.renamed_data["defense"][0]
            + self.renamed_data["sp_atk"][0]
            + self.renamed_data["sp_def"][0]
            + self.renamed_data["speed"][0]
        )
        self.assertEqual(transformed_df["total"][0], expected_total)

    def test_transform(self):
        transformed_df = self.transformer.transform(self.data.copy())
        expected_columns = [
            "id",
            "name",
            "type1",
            "type2",
            "total",
            "hp",
            "attack",
            "defense",
            "sp_atk",
            "sp_def",
            "speed",
            "generation",
            "is_legendary",
            "region",
            "can_evolve",
        ]
        if transformed_df is not None:
            self.assertEqual(list(transformed_df.columns), expected_columns)
        else:
            self.fail("Transform method returned None")
