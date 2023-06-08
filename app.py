from flask import Flask, render_template, request
from imdb import IMDb
from wikipedia import summary, exceptions

app = Flask(__name__)
ia = IMDb()

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for receiving user preferences and providing movie suggestions
@app.route('/suggest', methods=['POST'])
def suggest():
    # Get user preferences from the form
    genre = request.form.get('genre')
    min_rating = float(request.form.get('min_rating'))

    # Search for movies based on user preferences
    movies = ia.search_movie(genre)
    suggestions = []
    for movie in movies:
        ia.update(movie)
        if movie.get('rating') and movie['rating'] >= min_rating:
            try:
                movie_summary = summary(movie['title'], sentences=2)
                suggestions.append({
                    'title': movie['title'],
                    'rating': movie['rating'],
                    'image': movie.get('full-size cover url'),
                    'summary': movie_summary
                })
            except exceptions.DisambiguationError:
                # Handle DisambiguationError by skipping the movie
                continue
            except exceptions.PageError:
                # Handle PageError by adding a fallback message
                movie_summary = 'No data available'
                suggestions.append({
                    'title': movie['title'],
                    'rating': movie['rating'],
                    'image': movie.get('full-size cover url'),
                    'summary': movie_summary
                })

    # Render the suggestions template with the movie suggestions
    return render_template('suggestions.html', suggestions=suggestions)

if __name__ == '__main__':
    app.run(debug=True)
