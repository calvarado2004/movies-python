import psycopg2
import requests

'''
RapidAPI. (n.d.). IMDb8 API documentation. Retrieved [September 21, 2023], from https://rapidapi.com/apidojo/api/imdb8
'''


class IMDbAPI:

    def __init__(self, api_key):
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }
        self.querystring = {"q": " "}
        self.url = "https://imdb8.p.rapidapi.com/auto-complete"

    def search_movie(self, query):
        self.querystring['q'] = query
        response = requests.get(self.url, headers=self.headers, params=self.querystring)
        if response.status_code != 200:
            return []

        data = response.json()
        return [Movie(item) for item in data.get('d', []) if item.get('q') == 'feature']


class RetrieveMovies(IMDbAPI):
    def __init__(self, api_key, querystring):
        super().__init__(api_key)
        self.conn = psycopg2.connect(
            dbname="movies",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self.querystring = {"q": querystring}
        self.url = "https://imdb8.p.rapidapi.com/title/find"

    MAX_RESULTS = 10
    OFFSET = 0

    def fetch_movies(self):
        response = requests.get(self.url, headers=self.headers, params=self.querystring)
        data = response.json()

        for result in data['results']:
            id_movie = result.get('id', None)
            runningTimeInMinutes = result.get('runningTimeInMinutes', None)
            nextEpisode = result.get('nextEpisode', None)
            numberOfEpisodes = result.get('numberOfEpisodes', None)
            seriesEndYear = result.get('seriesEndYear', None)
            seriesStartYear = result.get('seriesStartYear', None)
            title = result.get('title', None)
            titleType = result.get('titleType', None)
            year = result.get('year', None)
            image = result.get('image', None)
            principals = result.get('principals', None)

            self.cursor.execute("""
                INSERT INTO titles (id, runningTimeInMinutes, nextEpisode, numberOfEpisodes, seriesEndYear, 
                seriesStartYear, title, titleType, year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT(id) DO NOTHING
            """, (id_movie, runningTimeInMinutes, nextEpisode, numberOfEpisodes, seriesEndYear, seriesStartYear, title,
                  titleType, year))

            if image:
                self.cursor.execute("""
                    INSERT INTO images (id, title_id, height, url, width)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT(id) DO NOTHING
    
                """, (result['image']['id'], result['id'], result['image']['height'], result['image']['url'],
                      result['image']['width']))

            if principals:
                for principal in result['principals']:
                    id_principal = principal.get('id', None)
                    id_movie = result.get('id', None)
                    legacyNameText = principal.get('legacyNameText', None)
                    name = principal.get('name', None)
                    category = principal.get('category', None)
                    endYear = principal.get('endYear', None)
                    episodeCount = principal.get('episodeCount', None)
                    startYear = principal.get('startYear', None)
                    roles = principal.get('roles', None)

                    self.cursor.execute("""
                        INSERT INTO principals (id, title_id, legacyNameText, name, category, endYear, episodeCount, 
                        startYear)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT(id) DO NOTHING
                    """, (id_principal, id_movie, legacyNameText, name, category, endYear, episodeCount, startYear))

                    if roles:
                        for role in principal['roles']:
                            principal_id = principal.get('id', None)
                            character = role.get('character', None)
                            characterId = role.get('characterId', None)
                            self.cursor.execute("""
                                INSERT INTO roles (principal_id, character, characterId)
                                VALUES (%s, %s, %s)
                            """, (principal_id, character, characterId))

            self.conn.commit()

    def list_movies(self):
        self.cursor.execute('''
        SELECT * FROM public.titles''')
        return self.cursor.fetchall()

    def get_title(self, title_id):
        self.cursor.execute('''
        SELECT * FROM public.titles WHERE id = %s''', (title_id,))
        return self.cursor.fetchone()

    def get_characters(self, title_id):
        self.cursor.execute('''
        SELECT * FROM public.principals WHERE title_id = %s''', (title_id,))
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


class Movie:
    def __init__(self, movie_data):
        self.title = movie_data.get('l')
        self.id = movie_data.get('id')
        self.year = movie_data.get('y')
        self.image = movie_data.get('i', {}).get('imageUrl')


def main():
    movie_to_search = "game of thrones"

    retrieved = RetrieveMovies("cdec029326msh63574431fd6e264p123047jsn98a65102db61", movie_to_search)
    try:
        retrieved.fetch_movies()
        movie = retrieved.get_title('/title/tt0944947/')
        if movie:
            print(f"Title: {movie[6]}")
        else:
            print("Movie not found.")
        characters = retrieved.get_characters('/title/tt0944947/')
        print("\nPrincipals:")
        for character in characters:
            print(character[3])
    finally:
        retrieved.close()


if __name__ == "__main__":
    main()
