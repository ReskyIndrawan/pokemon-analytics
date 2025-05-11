import unittest
import pandas as pd
from unittest.mock import patch
from src.etl.extractor import PokemonExtractor


class TestPokemonExtractor(unittest.TestCase):
    @patch("src.etl.extractor.pd.read_csv")
    def test_extract_success(self, mock_read_csv):
        # Mock the read_csv function to return a sample DataFrame
        mock_read_csv.return_value = pd.DataFrame(
            {
                "Name": ["Bulbasaur", "Ivysaur"],
                "Type 1": ["Grass", "Grass"],
                "Type 2": ["Poison", "Poison"],
            }
        )

        extractor = PokemonExtractor()
        data = extractor.extract()

        # Assertions
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["Name"][0], "Bulbasaur")

    @patch("src.etl.extractor.pd.read_csv")
    def test_extract_file_not_found(self, mock_read_csv):
        # Mock the read_csv function to raise a FileNotFoundError
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        extractor = PokemonExtractor()
        data = extractor.extract()

        # Assertion
        self.assertIsNone(data)

    @patch("src.etl.extractor.pd.read_csv")
    def test_extract_general_exception(self, mock_read_csv):
        # Mock the read_csv function to raise a general Exception
        mock_read_csv.side_effect = Exception("Some error")

        extractor = PokemonExtractor()
        data = extractor.extract()

        # Assertion
        self.assertIsNone(data)


if __name__ == "__main__":
    unittest.main()
