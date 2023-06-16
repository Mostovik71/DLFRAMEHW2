import streamlit as st
import pandas as pd
import random


@st.cache_data
def get_data():
    df = pd.read_csv('films_new.csv')
    return df


df = get_data()
df.replics = df.replics.apply(lambda x: eval(x) if isinstance(x, str) else x)
df.chrono = df.chrono.apply(lambda x: eval(x) if isinstance(x, str) else x)
df.characters = df.characters.apply(
    lambda x: eval(x) if isinstance(x, str) else x)
df.genres = df.genres.apply(lambda x: eval(x) if isinstance(x, str) else x)
df.names = df.names.apply(lambda x: eval(x) if isinstance(x, str) else x)
# st.title('Movie app')

labels = [
    'Positive',
    'Negative',
    'Neutral'
]
mapping = {i: k for i, k in enumerate(labels)}

st.sidebar.header('Выбор фильма и персонажа')
movie_title = st.sidebar.selectbox('Название фильма',
                                   df.movie_title.unique().tolist())

character = st.sidebar.selectbox('Персонаж',
                                 [' '] + df[
                                     df.movie_title == movie_title].names.explode().unique().tolist(),
                                 disabled=False)
movie_id_ = df.query('movie_title == @movie_title').movieID.unique().item()


def genres_stat(movie_id, character=None):
    df_final = df.query('movieID == @movie_id')
    df_final['emotion'] = df_final.replics.apply(
        lambda x: [random.randint(0, 2) for _ in x])
    df_final['emotion'] = df_final.emotion.apply(
        lambda x: [mapping[i] for i in x])
    df_final.reset_index(inplace=True, drop=True)
    df_final = df_final[['names', 'emotion']]
    df_final = df_final.explode(['names', 'emotion'])
    df_final = df_final.groupby('names')['emotion'].value_counts(
        normalize=True).to_frame('frequency')

    if character is not None:
        df_to_return = df_final.loc[character]
        df_to_return.index.names = ['Эмоция']
        return df_to_return.rename(columns={
            'frequency': f'Соотношение для персонажа {character}'})
    else:
        df_final.index.names = ['Персонаж', 'Эмоция']
        return df_final.rename(
            columns={'frequency': f'Соотношение'}) # т.к. персонажей в фильме может быть много, возвращаем в текстовом формате



st.header(f'Выбранный фильм: {movie_title}')
if character == ' ':
    st.subheader('Персонаж не выбран')
    st.write(genres_stat(movie_id_))
else:
    st.subheader(f'Выбранный персонаж: {character}')
    st.write(genres_stat(movie_id_, character))
