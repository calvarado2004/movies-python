import unittest
from movies import IMDbAPI, Movie

'''
RapidAPI. (n.d.). IMDb8 API documentation. Retrieved [September 21, 2023], from https://rapidapi.com/apidojo/api/imdb8
'''


class TestIMDbAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.api_key = "cdec029326msh63574431fd6e264p123047jsn98a65102db61"
        self.api = IMDbAPI(self.api_key)

    def test_integration_search_movie(self):
        result = self.api.search_movie("matrix")
        self.assertGreater(len(result), 0)
        self.assertIsInstance(result[0], Movie)
        titles = [movie.title for movie in result]
        self.assertIn("The Matrix Revolutions", titles)


if __name__ == "__main__":
    unittest.main()
