import pandas as pd
import streamlit as st

df = pd.read_csv("movies.csv")

df.names = df.names.apply(lambda x: eval(x))
df.replics = df.replics.apply(lambda x: eval(x))
emotions = ["Positive", "Neutral", "Negative"]

st.title("Интерфейс для аннотации диалогов")
movie = st.sidebar.selectbox('Выберите фильм',
                             df.movie_title.unique().tolist())

data = df.query("movie_title == @movie")
data["emotions"] = ""

for i, row in data.iterrows(): # Идем циклом по диалогам с выбранного фильма
    dialogues = ["{}: {}".format(name, replic) for name, replic in zip(row.names, row.replics)]
    dialogue_text = "\n\n".join(dialogues)
    st.write("Диалог № {} \n\n {}".format(i + 1, dialogue_text))

    emotions_selected = st.multiselect("Выберите эмоции для диалога № {}".format(i + 1),
                                       emotions)
    if len(emotions_selected):
        st.write("Выбранные эмоции:", emotions_selected)
    else:
        st.write("Пока нет выбранных эмоций")

    data.loc[i, "emotions"] = ", ".join(emotions_selected)

if st.button("Сохранить размеченные диалоги"):
    data.to_csv("dialogs_labeled.csv", index=False)
