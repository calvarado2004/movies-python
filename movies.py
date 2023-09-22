import requests

'''
RapidAPI. (n.d.). IMDb8 API documentation. Retrieved [September 21, 2023], from https://rapidapi.com/apidojo/api/imdb8
'''


class IMDbAPI:
    BASE_URL = "https://imdb8.p.rapidapi.com/auto-complete"

    def __init__(self, api_key):
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }
        self.querystring = {"q": " "}

    def search_movie(self, query):
        self.querystring['q'] = query
        response = requests.get(self.BASE_URL, headers=self.headers, params=self.querystring)
        if response.status_code != 200:
            return []

        data = response.json()
        return [Movie(item) for item in data.get('d', []) if item.get('q') == 'feature']


class Movie:
    def __init__(self, movie_data):
        self.title = movie_data.get('l')
        self.id = movie_data.get('id')
        self.year = movie_data.get('y')
        self.image = movie_data.get('i', {}).get('imageUrl')


def main():
    imdb_api = IMDbAPI("cdec029326msh63574431fd6e264p123047jsn98a65102db61")

    while True:
        query = input("\nEnter a movie name to search or 'exit' to quit: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        movies = imdb_api.search_movie(query)

        if not movies:
            print("No movies found for your search query.")
            continue

        print("\nFound movies:")
        for movie in movies:
            print(f"Title: {movie.title}, Year: {movie.year}, Image: {movie.image}")


if __name__ == "__main__":
    main()
