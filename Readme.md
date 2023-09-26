# Movie Search with IMDb8 API

A simple Python script that allows users to search for movies using the IMDb8 API.


## Author

- Carlos Alvarado Martinez

## Features

- Search for movies by name.
- Get movie details like title, year of release, and image link.

## Requirements

- Python 3.x
- Docker
- Docker Compose
- `requests` module. Install it using:

  ```bash
  pip install requests
  ```
- `psycopg2` module. Install it using:

  ```bash
  pip install psycopg2-binary
  ```
  

## Usage

You have to install Docker and Docker Compose to run the application.
  ```bash
    docker-compose up -d
    python3 movies.py
  ```

## Tests 

 - Unit tests:

  ```bash
    python3 -m unittest movies_unit_test.py
  ```
 - Integration tests:
  ```bash
    python3 -m unittest movies_integration_test.py
  ```
