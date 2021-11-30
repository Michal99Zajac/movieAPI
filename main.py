from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import random


app = FastAPI()

origins = [ "*" ]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)



API_KEY = "?api_key=159c3b33615afa1b3e782c8c1377013a"
API_URL = "https://api.themoviedb.org/3/"
MAX_ID = requests.get(f"{API_URL}movie/latest{API_KEY}").json()["id"]
GENRES = requests.get(f"{API_URL}genre/movie/list{API_KEY}").json()["genres"]

@app.get('/movie')
def get_movie(genre: str = "", rating: float = 0):
    if genre == "" and rating == 0:
        return get_random_movie()
    if genre != "" and rating >= 0 and rating < 10:
        return get_genre_movie(genre, rating)
    return {}

def get_random_movie():
    random_movie_request = make_random_movie_request()
    while random_movie_request.status_code == 404:
        random_movie_request = make_random_movie_request()
    title = random_movie_request.json()["title"]
    return { "value": title }

def make_random_movie_request():
    id = random.randrange(0, MAX_ID)
    return requests.get(f"{API_URL}movie/{id}{API_KEY}")

def get_genre_movie(genre, rating):
    genre_found = False
    for g in GENRES:
        if genre.lower() == g["name"].lower():
            id = g["id"]
            genre_found = True
            break
    
    if not genre_found:
        return {}
    
    return get_title_with_genre_and_rating(genre, rating)
        

def get_title_with_genre_and_rating(genre, rating):
    page = get_random_page(f"{API_URL}discover/movie{API_KEY}&with_genres={id}&vote_average.gte={rating}")
    title = get_title_from_discover(f"{API_URL}discover/movie{API_KEY}&with_genres={id}&vote_average.gte={rating}&page={page}")
    return { "value": title }

def get_random_page(url):
    genre_movie_request = requests.get(url)
    total_pages = genre_movie_request.json()["total_pages"]
    return random.randrange(1, total_pages)

def get_title_from_discover(url):
    genre_movie_request = requests.get(url)
    return genre_movie_request.json()["results"][0]["title"]

@app.get('/movie/type')
def get_type(movie):
    url = f"{API_URL}search/movie{API_KEY}&query={movie}"
    movie_type_request = requests.get(url)
    genre_ids = movie_type_request.json()["results"][0]["genre_ids"]
    genres = get_genres_by_ids(genre_ids)
    return { "value": ", ".join(genres) }

def get_genres_by_ids(genre_ids):
    genres = []
    for id in genre_ids:
        for genre in GENRES:
            if genre["id"] == id:
                genres.append(genre["name"])
    return genres