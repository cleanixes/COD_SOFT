import requests
from collections import defaultdict
import random

class MovieRecommender:
    def __init__(self, api_key):
        """
        Initialize the MovieRecommender with the TMDb API key.
        
        api_key: str, The API key for accessing TMDb API
        """
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.genres = self.getGenres()

    def getGenres(self):
        """
        Fetch all available movie genres from TMDb API.
        
        This method makes an API call to retrieve all movie genres and their corresponding IDs.
        It then creates a dictionary mapping genre IDs to genre names for easy lookup.
        
        response creates a print f url

        return: dict, A dictionary where keys are genre IDs and values are genre names
        takes ids and names and the for loop creates a dict mapping the two sections 
        returns a json object containing genres
        """
        url = f"{self.base_url}/genre/movie/list"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        return {genre['id']: genre['name'] for genre in response.json()['genres']}

    def getMovieDetails(self, movieId):
        """
        Retrieve detailed information about a specific movie from TMDb API.
        
        This method fetches comprehensive data about a movie, including its title, 
        release date, genres, overview, etc.
        
        params- is a dictionary containing the api key thats used for get requests which then in the resposne
        get formatted into a string in a get request to store the movie id in a json
        movieId- int, The TMDb ID of the movie
        return- A dictionary containing detailed information about the movie
        """
        url = f"{self.base_url}/movie/{movieId}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        return response.json()

    def getUserPreferences(self, liked_movies):
        """
        Analyze the user's genre preferences based on their liked movies.
        
        This method takes a list of movie IDs that the user has liked, fetches 
        details for each movie, and counts the occurrences of each genre. This 
        creates a profile of the user's genre preferences.
        
        likedMovies- A list of TMDb movie IDs that the user has liked
        return- defaultdict, A dictionary where keys are genre IDs and values are 
        the number of times each genre appeared in the liked movies
        """
        genrePreferences = defaultdict(int)
        for movieId in likedMovies:
            movie = self.getMovieDetails(movieId)
            for genreId in movie['genres']:
                genrePreferences[genreId['id']] += 1
        return genrePreferences

    def getRecommendations(self, genrePreferences, numRecommendations=5):
        """
        Generate movie recommendations based on the user's genre preferences.
        
        1. Sort the user's genre preferences to find their top genres.
        2. For each top genre, fetch popular movies in that genre.
        3. Randomly select a few movies from each genre to ensure diversity.
        4. Combine and shuffle the selections to produce the final recommendations.
        
        genrePreferences- dictionary of the user's genre preferences (output from getUserPreferences)
        numRecommendations- int, the number of movie recommendations to generate (default 5)
        A list of dictionaries, each containing details of a recommended movie

        Converts the dictionary into a tuple list, where each is a key and value pair, the lambda specifies theat the sorting
        is based on the second element of each value, lambda is a short function fyi in this case takes x and returns second element
        takes the list in descending order
        """
        recommendations = []
        
        sortedGenres = sorted(genrePreferences.items(), key=lambda x: x[1], reverse=True)
        topGenres = [genreId for genreId, _ in sortedGenres[:3]]

        for genreId in topGenres:
            url = f"{self.base_url}/discover/movie"
            params = {
                "api_key": self.api_key,
                "withGenres": genreId,
                "sortBy": "popularity.desc"
            }
            response = requests.get(url, params=params)
            movies = response.json()['results']
            recommendations.extend(random.sample(movies, min(3, len(movies))))

        return random.sample(recommendations, min(numRecommendations, len(recommendations)))

# Usage example
apiKey = "53e341ca3c1ded88aacaf16a1ea7819e"
recommender = MovieRecommender(apiKey)


likedMovies = [550, 238, 680]  # Fight Club, The Godfather, Pulp Fiction

# Get the user's genre preferences based on their liked movies
userPreferences = recommender.getUserPreferences(likedMovies)

# Generate recommendations based on the user's preferences
recommendations = recommender.getRecommendations(userPreferences)

print("Recommended movies:")
for movie in recommendations:
    print(f"- {movie['title']} ({movie['release_date'][:4]})")
