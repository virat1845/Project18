import pickle
import streamlit as st
import requests
import time
import requests
import pickle


# Function to fetch movie poster with retries and timeout
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    for _ in range(3):  # Try 3 times in case of failure
        try:
            data = requests.get(url, timeout=10)  # Set timeout to 10 seconds
            data.raise_for_status()  # Raise an error if the request fails
            data = data.json()

            poster_path = data.get('poster_path', None)

            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
            else:
                # Return a default image if no poster is available
                return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(5)  # Wait 5 seconds before retrying
    return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"  # Return fallback image after retries


# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # Fetch the movie poster and title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit header and layout
st.header('Movie Recommender System')

# Load movie data and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie list for selection
movie_list = movies['title'].values

# Movie selection from dropdown
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Recommendation button
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create columns for displaying recommendations
    col1, col2, col3, col4, col5 = st.columns(5)  # updated from beta_columns
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

