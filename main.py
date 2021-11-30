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
def get_movie(genre = "", rating = ""):
    if genre == "" and rating == "":
        print("random")
        return get_random_movie()
    if genre != "" and rating == "":
        print("genre")
        return get_genre_movie(genre)
    return None

def get_random_movie():
    random_movie_request = make_random_movie_request()
    while random_movie_request.status_code == 404:
        random_movie_request = make_random_movie_request()
    title = random_movie_request.json()["title"]
    return { "value": title }

def make_random_movie_request():
    id = random.randrange(0, MAX_ID)
    return requests.get(f"{API_URL}movie/{id}{API_KEY}")

def get_genre_movie(genre):
    genre_found = False
    for g in GENRES:
        if genre.lower() == g["name"].lower():
            id = g["id"]
            genre_found = True
            break
    
    if not genre_found:
        return None

    page = get_random_page(id)
    title = get_title_from_genre(id, page)
    return { "value": title }


def get_random_page(id):
    genre_movie_request = requests.get(f"{API_URL}discover/movie{API_KEY}&with_genres={id}")
    total_pages = genre_movie_request.json()["total_pages"]
    return random.randrange(1, total_pages)

def get_title_from_genre(id, page):
    genre_movie_request = requests.get(f"{API_URL}discover/movie{API_KEY}&with_genres={id}&page={page}")
    return genre_movie_request.json()["results"][0]["title"]
    