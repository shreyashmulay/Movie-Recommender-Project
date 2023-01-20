from unicodedata import name
from urllib import response
import streamlit as st
import pickle
import pandas as pd
import requests
st.title("Movie Recommendation Site")


def fetch_poster(movie_poster):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=a19a82a4388350e19224a682bb495ab1&language=en-US'.format(movie_poster))
    data = response.json()

    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_poster = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        # fetch poster
        recommended_movies_posters.append(fetch_poster(movie_poster))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['original_title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
