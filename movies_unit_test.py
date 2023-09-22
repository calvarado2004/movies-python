import unittest
from unittest.mock import patch, Mock
from movies import IMDbAPI, Movie

'''
RapidAPI. (n.d.). IMDb8 API documentation. Retrieved [September 21, 2023], from https://rapidapi.com/apidojo/api/imdb8
'''


class TestIMDbAPIUnit(unittest.TestCase):
    def setUp(self):
        self.api_key = "this-is-a-mock-api-key"
        self.api = IMDbAPI(self.api_key)

    @patch('requests.get')
    def test_search_movie(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "d": [
                {
                    "l": "Game of Thrones",
                    "id": "tt0944947",
                    "y": 2011,
                    "q": "feature",
                    "i": {"imageUrl": "sample_url"}
                }
            ]
        }
        mock_get.return_value = mock_response

        result = self.api.search_movie("game of thr")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Game of Thrones")


if __name__ == "__main__":
    unittest.main()
