import streamlit as st
import pickle
import numpy as np
import requests

#HuggigFace URLs
movies_url="https://huggingface.co/DevenderMathela/movie-recommender-model/resolve/main/movies.pkl"
similarity_url="https://huggingface.co/DevenderMathela/movie-recommender-model/resolve/main/similarity.pkl"


# Function to load pickle from URL
def load_pickle(url):
    response = requests.get(url)
    return pickle.loads(response.content)

# Cache the model (very important)
@st.cache_resource
def load_data():
    movies_df = load_pickle(movies_url)
    similarity = load_pickle(similarity_url)
    return movies_df, similarity


movies_df, similarity = load_data()


def fetch_poster(movie_id):
    api_key= "5fff3e122512356c3c62797c28a0a8be"
    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index=movies_df[movies_df['title']==movie].index[0]
    distances=similarity[movie_index]
    sorted_movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies_poster = []
    recommended_movies=[]
    for i in sorted_movies_list:
        movie_id=movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_poster



movies_titles=movies_df['title'].values

st.title('Movie Recommendation System')


selected_movie_name= st.selectbox(
    "Choose a movie",
    movies_titles
)

if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)

    col1, col2, col3, col4, col5= st.columns(5)
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

