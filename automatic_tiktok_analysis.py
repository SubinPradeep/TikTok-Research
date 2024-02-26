import os
import openai
import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

st.title("Automatic Misinformation Analysis")

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""
if "check_done" not in st.session_state:
    st.session_state["check_done"] = False

if not st.session_state["check_done"]:
    # Display input for OpenAI API key
    st.session_state["api_key"] = st.text_input('Enter the OpenAI API key', type='password')

# OpenAI Completion request for checking API key
def is_api_key_valid(api_key):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Hello World!"},
  ]
)
    except:
        return False
    else:
        return True

if st.session_state["api_key"]:
    # On receiving the input, perform an API key check
    if is_api_key_valid(st.session_state["api_key"]):
        # If API check is successful
        st.success('OpenAI API key check passed')
        st.session_state["check_done"] = True
        client = OpenAI(api_key=st.session_state["api_key"])
    else:
        # If API check fails
        st.error('OpenAI API key check failed. Please enter a correct API key')

def get_model_selection():
    # Display model selection after API key check passed
    model = st.selectbox("Select the AI model to use:", ("gpt-3.5-turbo", "gpt-3.5-turbo-1106", "gpt-4", "gpt-4-1106-preview"))
    return model

if st.session_state["check_done"]:
    # Display model selection after API key check passed
    selected_model = get_model_selection()

video_files = st.file_uploader('Upload Your Video File', type=['wav', 'mp3', 'mp4'], accept_multiple_files=True)

#openai.api_key = 

def transcribe(video_file):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=video_file, 
        response_format="text"
    )
    return transcript

def analyze(transcript, model):
    system_msg1 = "Your task is to extract up to six keywords from the text provided to you, sorted in order of criticality. Follow the format \"Keywords: ...\""

    system_msg2 = "Your next task is to determine if the text contains any misinformation. You only could say \'May contain misinformation\', \'Cannot be recognized\' or \'No misinformation detected\'."

    system_msg3 = "Lastly, you must briefly summarize the reasons for determining whether the statement contains misinformation. Provide three or less reasons of no more than 50 words each."

    chat_sequence = [
        {"role": "system", "content": "You are an experienced scientist and medical doctor. You need to fully read and understand the text paragraph given below. Then complete the requirements based on the contents therein." + transcript},
        {"role": "user", "content": system_msg1},
        {"role": "user", "content": system_msg2},
        {"role": "user", "content": system_msg3}
    ]   

    response = client.chat.completions.create(
        model=model,
        #response_format={ "type": "json_object" },
        messages=chat_sequence
    )

    gpt_response = response.choices[0].message.content
    return gpt_response

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def keyword(keywords):
    keywords_list = [keyword.strip() for keyword in keywords.split(',')]

    # Count occurrences of each unique keyword
    keyword_counts = {keyword: keywords_list.count(keyword) for keyword in set(keywords_list)}

    # Create a dataframe from the results
    df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Occurrences'])
    st.dataframe(df)

if st.button('Transcribe and Analyze Videos'):
    transcipt_status = False
    data = []
    keywords = ""
    for video_file in video_files:
        print(video_file.name)
        if video_file is not None:
            transcript = transcribe(video_file)
            analysis = analyze(transcript, selected_model)
            st.markdown(video_file.name + ": " + transcript)
            st.markdown(video_file.name + ": " + analysis)

            # Split the analysis information
            analysis = analysis.split('\n')
            misinformation_status = analysis[0]
            keywords_index = [i for i, element in enumerate(analysis) if 'Keywords:' in element]
            if keywords_index:
                video_keywords = analysis[keywords_index[0]]
                video_keywords = video_keywords.split("Keywords:")[1]
                print(video_keywords)
                keywords += video_keywords
                print(video_keywords)
                keyword(video_keywords)
            else:
                video_keywords = "Not found"
            #reasons = ' '.join(analysis[4:])


            d = {
                "video_file": video_file.name,
                "transcript": transcript, 
                "misinformation_status": misinformation_status, 
                "keywords": video_keywords, 
                #"reasons": reasons
            }
            data.append(d)
            #print('"{}"'.format(transcript))        
        else:
            st.sidebar.error("Please upload a video file")

    df = pd.DataFrame(data)
    keyword(keywords)
    csv = convert_df(df)
    date_today_with_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name = f'results_{date_today_with_time}.csv',
        mime='text/plain',
    )