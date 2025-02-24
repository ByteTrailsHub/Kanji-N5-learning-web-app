import streamlit as st
import pandas as pd
import random


# Load Kanji Data
@st.cache_data
def load_kanji_data():
    return pd.read_csv("kanji_vocab.csv")


kanji_df = load_kanji_data()

# App Title
st.title("Kanji Learning App")

# Sidebar Navigation
menu = st.sidebar.radio("Select Mode", ["Reference", "Quiz"])

if menu == "Reference":
    st.header("Kanji Reference Table")
    st.dataframe(kanji_df)

elif menu == "Quiz":
    quiz_type = st.radio("Select Quiz Type", ["Multiple Choice", "Typing"], index=0)
    quiz_mode = st.radio("Test on", ["Pronunciation", "Meaning"], index=0)

    if "random_kanji" not in st.session_state:
        st.session_state.random_kanji = kanji_df.sample(1).iloc[0]
        st.session_state.submitted = False

    random_kanji = st.session_state.random_kanji
    correct_answer = random_kanji["Hiragana"] if quiz_mode == "Pronunciation" else random_kanji["English Meaning"]

    st.subheader(f"What is the {quiz_mode.lower()} of: {random_kanji['Kanji']}?")

    if quiz_type == "Multiple Choice":
        if "options" not in st.session_state:
            options = kanji_df.sample(3)["Hiragana" if quiz_mode == "Pronunciation" else "English Meaning"].tolist()
            options.append(correct_answer)
            random.shuffle(options)
            st.session_state.options = options

        choice = st.radio("Choose the correct answer:", st.session_state.options)
        if st.button("Submit"):
            if choice == correct_answer:
                st.success("Correct!")
            else:
                st.error(f"Wrong! The correct answer is {correct_answer}")
            st.session_state.submitted = True

    elif quiz_type == "Typing":
        user_input = st.text_input("Type your answer:")
        if st.button("Submit"):
            if user_input.strip().lower() == correct_answer.strip().lower():
                st.success("Correct!")
            else:
                st.error(f"Wrong! The correct answer is {correct_answer}")
            st.session_state.submitted = True

    if st.session_state.submitted:
        if st.button("Next Question"):
            st.session_state.random_kanji = kanji_df.sample(1).iloc[0]
            st.session_state.submitted = False
            st.session_state.pop("options", None)
