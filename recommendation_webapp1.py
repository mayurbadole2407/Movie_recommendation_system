import streamlit as st
import pickle
import requests
from PIL import Image
import base64

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(select_movie_name):
    li = []
    poster=[]
    overview=[]
    index = movies[movies['title'] == select_movie_name].index[0]
    distances = similarity[index]
    distances = list(enumerate(distances))
    # now we sorting the movies similarity
    distances = sorted(distances, reverse=True, key=lambda x: x[1])
    movies_list = distances[1:6]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster.append(poster_fecth(movie_id))
        overview.append((overview_fecth(movie_id)))
        li.append(movies.iloc[i[0]].title)
    return li, poster, overview

def poster_fecth(movie_index):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eac64aa791156f552dda5c7d28fb7825'.format(movie_index))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def overview_fecth(movie_index):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=eac64aa791156f552dda5c7d28fb7825'.format(movie_index))
    data = response.json()
    return data['overview']


def main():
    def hide_main_menu_style():
        hide_main_menu = '''
        <style>
        #MainMenu {visibility: hidden;}
        footer{visibility: hidden;}
        </style>
        '''
        st.markdown(hide_main_menu, unsafe_allow_html=True)

    hide_main_menu_style()
    # st.image(image)
    # st.sidebar.markdown('side')
    st.title('Movie Recommendation')
    list_m=[]
    for i in movies.title:
        list_m.append(i)
    select_movie_name = st.selectbox(
    'Select Your Movie',
    (list_m))

    if st.button('Submit'):
        recomm_movies, posters, overview = recommend(select_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recomm_movies[0])
            st.image(posters[0],caption=overview[0])

        with col2:
            st.text(recomm_movies[1])
            st.image(posters[1],caption=overview[1])
        with col3:
            st.text(recomm_movies[2])
            st.image(posters[2],caption=overview[2])
        with col4:
            st.text(recomm_movies[3])
            st.image(posters[3],caption=overview[3])
        with col5:
            st.text(recomm_movies[4])
            st.image(posters[4],caption=overview[4])

if __name__=='__main__':
    main()