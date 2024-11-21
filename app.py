from flask import Flask, jsonify, request, redirect, render_template, session, url_for, flash, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


CORS(app, supports_credentials=True, origins=["http://localhost:3000"])


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return response



app.config['SECRET_KEY'] = 'DAfense101!!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://afockens:DAfense101!!@users-db.cl0ukeemwuxg.us-east-2.rds.amazonaws.com:3306/accounts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cookies across domains
app.config['SESSION_COOKIE_SECURE'] = True







db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):

        self.password_hash = generate_password_hash(password)
        print("storing hashed password: ",self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # e.g., "movie" or "show"
    movie_id = db.Column(db.Integer, nullable=False)  # Add this field for the TMDB ID
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))

with app.app_context():
    db.create_all()

def is_logged_in():
    return 'user_id' in session

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password = password.strip()
        # Validate input
        if not username or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400

        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Create new user
        new_user = User(username=username, email=email)

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        session.permanent = True
        return jsonify({'message': 'Account created successfully'}), 201

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session.permanent = True
        print("logged in as ",session['user_id'])
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        # Ensure the session is refreshed
        db.session.flush()

        # Query all users
        users = User.query.all()

        # Format user data
        user_list = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email
            } for user in users
        ]

        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

































#FOR THE MOVIE API's


api_key = "630b4e7c293ad229ae05e63103af19fe"
headers = {
    'User-Agent': 'Mozilla/5.0'  # Mimics a browser request
}

# GET FUNCTIONS

def get_genre_id(desired_genre, media_type):
    """Get the genre ID for the specified genre and media type (movie or tv)."""
    genres_url = f"https://api.themoviedb.org/3/genre/{media_type}/list?api_key={api_key}"
    genres_response = requests.get(genres_url, headers=headers)
    genres_response.raise_for_status()
    genres_data = genres_response.json()
    return next((genre['id'] for genre in genres_data['genres'] if genre['name'].lower() == desired_genre.lower()), None)


def get_show_id(show_name):
    """Retrieve the TMDB ID of a TV show by name."""
    search_url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={show_name}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data['results']:
        return None  
    
    return data['results'][0]['id'] 

def get_movie_id(movie_name):
    """Retrieve the TMDB ID of a Movie by name."""
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data['results']:
        return None  
    
    return data['results'][0]['id'] 


def get_actor_id(actor_name):
    """Retrieve the TMDB ID of an actor by name."""
    search_url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if not data['results']:
        return None  # No actor found with that name
    
    return data['results'][0]['id']


def get_actor_top_movies(actor_id, genre_id=None):
    """Retrieve and sort an actor's movies by rating, with an optional genre filter."""
    credits_url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}"
    response = requests.get(credits_url, headers=headers)
    response.raise_for_status()
    credits_data = response.json()

    # Filter and sort movies
    top_movies = sorted(
        (
            movie for movie in credits_data['cast'] 
            if (movie.get('vote_average') is not None and 
                (genre_id is None or genre_id in movie.get('genre_ids', [])))
        ),
        key=lambda x: x['vote_average'],
        reverse=True
    )

    # Format and return the top-rated movies
    return [
        {
            "title": movie['title'],
            "rating": movie['vote_average'],
            "release_date": movie.get('release_date', 'N/A'),
            "description": movie['overview']
        }
        for movie in top_movies
    ]


def get_most_popular_episode(tv_id):
    """Find the most popular episode of a TV show given its TMDB ID."""
    show_details_url = f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={api_key}"
    response = requests.get(show_details_url, headers=headers)
    response.raise_for_status()
    show_data = response.json()

    most_popular_episode = None
    max_popularity = 0

    # Loop through each season and each episode to find the most popular one
    for season in show_data['seasons']:
        season_number = season['season_number']
        season_url = f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={api_key}"
        season_response = requests.get(season_url, headers=headers)
        season_response.raise_for_status()
        season_data = season_response.json()

        for episode in season_data['episodes']:
            if episode['popularity'] > max_popularity:
                max_popularity = episode['popularity']
                most_popular_episode = {
                    "season": season_number,
                    "episode": episode['episode_number'],
                    "title": episode['name'],
                    "popularity": episode['popularity'],
                    "description": episode['overview']
                }
    
    return most_popular_episode

# API ENDPOINTS

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    title = request.args.get('title')  # The title to base recommendations on
    min_rating = float(request.args.get('min_rating', 7.0))  # Minimum rating, default 7.0
    desired_genre = request.args.get('genre')  # Optional genre filter
    media_type = request.args.get('media_type')  # 'movie' or 'tv'

    # Debugging: Print initial values
    print(f"Request received for title: {title}, min_rating: {min_rating}, genre: {desired_genre}, media_type: {media_type}")

    # Check for required media_type parameter
    if media_type not in ['movie', 'tv']:
        print("Error: Invalid media_type")
        return jsonify({"error": "media_type parameter must be either 'movie' or 'tv'."}), 400

    # Step 1: Get the genre ID for the specified genre, if provided
    genre_id = get_genre_id(desired_genre, media_type) if desired_genre else None
    print(f"Genre ID resolved to: {genre_id}")

    # Step 2: Search for the media title and get its ID
    if media_type == 'tv':
        media_id = get_show_id(title)
    else:
        media_id = get_movie_id(title)

    if media_id is None:
        print(f"Error: {media_type.title()} '{title}' not found.")
        return jsonify({"error": f"{media_type.title()} '{title}' not found."}), 404

    print(f"{media_type.title()} ID resolved to: {media_id}")

    # Step 3: Get recommendations based on the media ID
    recommendations_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/recommendations?api_key={api_key}"
    recommendations_response = requests.get(recommendations_url, headers=headers)
    recommendations_response.raise_for_status()
    recommendations_data = recommendations_response.json()
    print(f"Received {len(recommendations_data['results'])} recommendations")

    # Step 4: Filter recommendations by rating and genre, if genre is provided
    filtered_recommendations = [
        {
            "title": item['title'] if media_type == 'movie' else item['name'],
            "rating": item['vote_average'],
            "description": item['overview']
        }
        for item in recommendations_data['results']
        if item['vote_average'] >= min_rating and (genre_id is None or genre_id in item.get('genre_ids', []))
    ]

    print(f"Filtered down to {len(filtered_recommendations)} recommendations after applying rating and genre filters")
    return jsonify(filtered_recommendations)

# Other endpoints remain the same as before




# WILL RETURN A LIST OF POSSIBLE MEDIA BASED ON A SEARCH
@app.route('/search_media', methods=['GET'])
def search_media():
    print("Session data:", session)
    print("searched as ",session['user_id'])
    query = request.args.get('query')
    media_type = request.args.get('media_type', 'movie')  # Default to movie if not specified
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    search_url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={query}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    search_results = response.json().get('results', [])

    # Format results to send back to the frontend
    formatted_results = [
        {
            'id': item['id'],  # Include the TMDB ID
            'title': item.get('title') or item.get('name'),
            'description': item.get('overview'),
            'release_date': item.get('release_date') or item.get('first_air_date'),
            'rating': item.get('vote_average'),
        }
        for item in search_results
    ]
    return jsonify(formatted_results)


#CREATES A FAVORITE TO ADD TO THE DATABASE
@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    print("Session data:", session)
    if not is_logged_in():
        print("says not logged in")
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    title = data.get('title')
    media_type = data.get('media_type')
    movie_id = data.get('movie_id')

    if not title or not media_type or not movie_id:
        return jsonify({'error': 'Title, media_type, and movie_id are required'}), 400

    # Add the favorite
    favorite = Favorite(user_id=session['user_id'], title=title, media_type=media_type, movie_id=movie_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': f'{media_type.title()} "{title}" added to favorites'}), 201


@app.route('/get_favorites', methods=['GET'])
def get_favorites():
    if not is_logged_in():
        return jsonify({'error': 'User not logged in'}), 401

    # Get the current user's favorites
    favorites = Favorite.query.filter_by(user_id=session['user_id']).all()
    favorites_list = [
        {'id': fav.id, 'title': fav.title, 'media_type': fav.media_type, 'movie_id': fav.movie_id}
        for fav in favorites
    ]
    return jsonify(favorites_list), 200














# RUNNING FLASK

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    