from flask import Flask, render_template, request
from imdb import IMDb
from math import ceil

app = Flask(__name__)
ia = IMDb()

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for receiving user preferences and providing movie suggestions
@app.route('/suggest', methods=['POST', 'GET'])
def suggest():
    if request.method == 'POST':
        genre = request.form.get('genre')
        min_rating = float(request.form.get('min_rating'))
        movies = ia.search_movie(genre)
        suggestions = []
        for movie in movies:
            ia.update(movie)
            if movie.get('rating') and movie['rating'] >= min_rating:
                suggestions.append(movie)
        page = 1
    else:
        page = request.args.get('page', default=1, type=int)
        genre = None
        min_rating = None
        suggestions = []

    per_page = 6  # Number of suggestions per page
    total_pages = int(ceil(len(suggestions) / per_page))
    start = (page - 1) * per_page
    end = start + per_page
    suggestions = suggestions[start:end]

    if not suggestions and page != 1:
        return render_template('suggestions.html', suggestions=suggestions, page=1, total_pages=total_pages, error="No more suggestions found.")

    return render_template('suggestions.html', suggestions=suggestions, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run()
