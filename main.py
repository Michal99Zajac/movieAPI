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

api_key = "?api_key=159c3b33615afa1b3e782c8c1377013a"
api_url = "https://api.themoviedb.org/3/"

@app.get('/movie')
def index():
    random_movie_request = make_random_movie_request()
    while random_movie_request.status_code == 404:
        random_movie_request = make_random_movie_request()
    title = random_movie_request.json()["title"]
    return { "value": title }

def get_random_id():
    max_id_request = requests.get(f"{api_url}movie/latest{api_key}")
    max_id = max_id_request.json()["id"]
    min_id = 0
    return random.randrange(min_id, max_id)

def make_random_movie_request():
    id = get_random_id()
    return requests.get(f"{api_url}movie/{id}{api_key}")