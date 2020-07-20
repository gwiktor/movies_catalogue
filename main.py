from flask import Flask, render_template, url_for, request
import tmdb_client

app = Flask(__name__)

@app.route('/')
def homepage():
    movie_lists = ['now_playing', 'popular', 'top_rated', 'upcoming']
    selected_list = request.args.get('list_type', "popular")
    if selected_list not in movie_lists:
        selected_list = 'popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movie_lists=movie_lists)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    def tmdb_title_url(path):
        return tmdb_client.get_movie_info(path)
    def tmdb_imageb_url(path, size):
        return tmdb_client.get_image_url(path, size)
    return {"tmdb_title_url": tmdb_title_url, "tmdb_image_url": tmdb_image_url, "tmdb_imageb_url": tmdb_imageb_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
   details = tmdb_client.get_single_movie(movie_id)
   cast = tmdb_client.get_single_movie_cast(movie_id, how_many=4)
   return render_template("movie_details.html", movie=details, cast=cast)



if __name__ == '__main__':
    app.run(debug=True)