import streamlit as st
import numpy as np
import requests
from dotenv import load_dotenv
load_dotenv()
import os
from utils import debounce_replicate_run
from auth0_component import login_button
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

#Global variables
REPLICATE_API_TOKEN = os.environ.get('REPLICATE_API_TOKEN', default='')
REPLICATE_MODEL_ENDPOINT7B = os.environ.get('REPLICATE_MODEL_ENDPOINT7B', default='')
REPLICATE_MODEL_ENDPOINT13B = os.environ.get('REPLICATE_MODEL_ENDPOINT13B', default='')
REPLICATE_MODEL_ENDPOINT70B = os.environ.get('REPLICATE_MODEL_ENDPOINT70B', default='')
PRE_PROMPT = "You are a helpful assistant, and respond once. The user is trying to learn more about a video by asking questions related to its content. Begin your answer with the timestamp of where the question's topic can be found. You have access to a transcript of the video, which contains the text spoken at different timestamps. If a user asks a question that is not related to the video transcript provided to you, then just simply ask the user to ask a question related to the video."

#Auth0
AUTH0_CLIENTID = os.environ.get('AUTH0_CLIENTID', default='')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', default='')

if not (REPLICATE_API_TOKEN and REPLICATE_MODEL_ENDPOINT13B and REPLICATE_MODEL_ENDPOINT7B and 
        AUTH0_CLIENTID and AUTH0_DOMAIN):
    st.warning("Add a `.env` file to your app directory with the keys specified in `.env_template` to continue.")
    st.stop()

#UI configuration
st.set_page_config(page_title="LLaMA2 Chatbot by a16z-infra", page_icon="🦙", layout="wide")
def render_app():
    custom_css = """
        <style>
            .stTextArea textarea {font-size: 13px;}
            div[data-baseweb="select"] > div {font-size: 13px !important;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    #header
    st.sidebar.header("SeekNSpot \nSeek the Questions, Spot the Answers - Intelligent Video Navigation Starts Here!")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    #Initialize Session State variables
    if 'chat_dialogue' not in st.session_state:
        st.session_state['chat_dialogue'] = []
    if 'llm' not in st.session_state:
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT70B
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.1
    if 'top_p' not in st.session_state:
        st.session_state['top_p'] = 0.9
    if 'max_seq_len' not in st.session_state:
        st.session_state['max_seq_len'] = 512
    if 'pre_prompt' not in st.session_state:
        st.session_state['pre_prompt'] = PRE_PROMPT
    if 'string_dialogue' not in st.session_state:
        st.session_state['string_dialogue'] = ''

    with open('youtube_url.text', 'r') as file:
        youtube_url = file.read()
    parsed_url = urlparse(youtube_url)
    videoKey = parse_qs(parsed_url.query)['v'][0]
    data = YouTubeTranscriptApi.get_transcript(videoKey)

    selected_goal = st.sidebar.selectbox('Choose Your Goal:', ['Learn', 'Quiz Me', 'Summarize', 'Translate'], key='goal')
    s = ""

    #Dropdown menu to select goal
    if selected_goal == 'Learn':
        st.session_state['pre_prompt'] = PRE_PROMPT
        s = "Type your question here to learn"
    elif selected_goal == 'Quiz Me':
        st.session_state['pre_prompt'] = "You are a helpful assistant. Your job is to ask questions based on the content of the video. The questions needs to be concise in a multiple choice format. If the user selects the wrong answer, then provide the timestamp in the video where they can learn about the topic."
        s = "Enter 'q' to get a question"
    elif selected_goal == 'Summarize':
        st.session_state['pre_prompt'] = "You are a helpful assistant. Your job is summarize the video transcript into bullet points. Each bullet point should be a relevant main idea or important detail from the video."
        s = "Enter 's' to get a summary"
    elif selected_goal == 'Translate':
        st.session_state['pre_prompt'] = "You are a helpful assistant, and respond once. The user is trying to learn more about a video by asking questions related to its content. You have access to a transcript of the video, which contains the text spoken at different timestamps. Begin your answer with a citation of the video transcript line where the answer is." 
        selected_language = st.selectbox('Language:', ['en', 'es', 'ko', 'hi', 'ja', 'ru'], key='lang')
        selected_data = YouTubeTranscriptApi.get_transcript(videoKey, languages=[selected_language, 'en'])
        st.markdown("Video Transcript in Your Desired Language (Defaults to English if Not Found)")
        for selected_row in selected_data:
            st.markdown(str(selected_row['start']) + " seconds: " + str(selected_row['text']))
        s = "Type your question here to learn"

    transcript = "\n--- Video Transcript ---\n"
    for row in data:
        transcript += f"{row['start']} seconds: {row['text']}\n"
    st.session_state['pre_prompt'] += transcript

    #Dropdown menu to select the model endpoint
    selected_option = st.sidebar.selectbox('Choose a LLaMA2 model:', ['LLaMA2-70B', 'LLaMA2-13B', 'LLaMA2-7B'], key='model')
    if selected_option == 'LLaMA2-7B':
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT7B
    elif selected_option == 'LLaMA2-13B':
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT13B
    else:
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT70B

    #Model hyper parameters
    st.session_state['temperature'] = st.sidebar.slider('Temperature:', min_value=0.01, max_value=5.0, value=1.0, step=0.01)
    st.session_state['top_p'] = st.sidebar.slider('Top P:', min_value=0.01, max_value=1.0, value=0.8, step=0.01)
    st.session_state['max_seq_len'] = st.sidebar.slider('Max Sequence Length:', min_value=64, max_value=16384, value=8192, step=64)

    btn_col1, btn_col2, btn_col3 = st.sidebar.columns(3)

    # Clear Chat History button 
    def clear_history():
        st.session_state['chat_dialogue'] = []
    clear_chat_history_button = btn_col1.button("Clear History",
                                            use_container_width=True,
                                            on_click=clear_history)

    # add logout button
    def logout():
        del st.session_state['user_info']
    logout_button = btn_col2.button("Logout",
                                use_container_width=True,
                                on_click=logout)
        
    #logo
    st.sidebar.image('seeknspot.png')

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_dialogue:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input(s):
        # Add user message to chat history
        if selected_goal == 'Quiz Me' and prompt == "q":
            st.session_state.chat_dialogue.append({"role": "user", "content": "Give me a question"})
        elif selected_goal == 'Summarize' and prompt == "s":
             st.session_state.chat_dialogue.append({"role": "user", "content": "Summarize the video"})
        else:
            st.session_state.chat_dialogue.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            string_dialogue = st.session_state['pre_prompt']
            for dict_message in st.session_state.chat_dialogue:
                if dict_message["role"] == "user":
                    string_dialogue = string_dialogue + "User: " + dict_message["content"] + "\n\n"
                else:
                    string_dialogue = string_dialogue + "Assistant: " + dict_message["content"] + "\n\n"
            output = debounce_replicate_run(st.session_state['llm'], string_dialogue + "Assistant: ",  st.session_state['max_seq_len'], st.session_state['temperature'], st.session_state['top_p'], REPLICATE_API_TOKEN)
            for item in output:
                full_response += item
                message_placeholder.markdown(full_response + "▌")
            x = np.array(full_response.split())
            res = []
            for i in range(len(x) - 1):
                if "seconds" in x[i+1]:
                    print(x[i])
                    res.append(float(x[i]))
            # Create a button in Streamlit to trigger the process
            try:
                reconstructed_url = f"https://www.youtube.com/watch?v={videoKey}&t={round(res[0])}s"
                backend_url = "http://localhost:5001/send-url"
                response = requests.post(backend_url, json={"url": reconstructed_url})
            except:
                print("No float found")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        print(full_response)
        st.session_state.chat_dialogue.append({"role": "assistant", "content": full_response})

if 'user_info' in st.session_state:
    render_app()
else:
    st.write("Please login to use the app. This is just to prevent abuse, we're not charging for usage.")
    st.session_state['user_info'] = login_button(AUTH0_CLIENTID, domain = AUTH0_DOMAIN)