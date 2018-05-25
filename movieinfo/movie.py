import requests
import json

api_key=" "
def movie_db(movie_name="avengers"):
    url = requests.get("https://api.themoviedb.org/3/search/movie?&api_key=" + api_key +"&query=" + movie_name)

    f_json = url.json()
    """   print(type(f_json["results"]))
    for movie in f_json["results"]:
        print(movie['title'])
        print(movie['overview'])
        print(movie['release_date'])
        if movie['backdrop_path']:
            print("https://canalpelis.com/wp-content/uploads" + movie['backdrop_path'])
    """
    path = f_json["results"]
    for i in range(len(path)):
        if (path[i]["backdrop_path"]):
            path[i]["backdrop_path"] = ("https://image.tmdb.org/t/p/original" + path[i]['backdrop_path'])
        """ for movie in f_json["results"]:
        if movie['backdrop_path']:
            path.append("https://canalpelis.com/wp-content/uploads" + movie['backdrop_path'])
        else:
            path.append('none')"""
    return path
