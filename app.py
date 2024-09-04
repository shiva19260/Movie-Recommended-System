import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(id):
    # Fetch movie details from TMDb API
    url = f'https://api.themoviedb.org/3/movie/{id}?api_key=e7002a78bb78ad632273967cabfa5a71&language=en-US'
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    data = response.json()

    # Check if 'poster_path' exists and is not None
    if 'poster_path' in data and data['poster_path']:
        poster_url = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        poster_url = "https://via.placeholder.com/500x750?text=Poster+Not+Available"
    return poster_url
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(names[idx])
            st.image(posters[idx])

