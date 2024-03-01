import os
import openai
import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI
import tiktoken
from pydub import AudioSegment
import ffmpeg
import subprocess
import sys

st.title("Tester")

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
    model = st.selectbox("Select the AI model to use:", ("gpt-3.5-turbo", "gpt-3.5-turbo-0125",  "gpt-3.5-turbo-1106", "gpt-4", "gpt-4-1106-preview", "gpt-4-0125-preview"))
    return model

if st.session_state["check_done"]:
    # Display model selection after API key check passed
    selected_model = get_model_selection()

video_file = st.file_uploader('Upload Your Video File', type=['wav', 'mp3', 'mp4'], accept_multiple_files=True)



def transcribe(video_file):
    for video_file in video_file:
        # try:
        #     # Attempt to call the API with the original file
        #     transcript = client.audio.transcriptions.create(
        #         model="whisper-1",
        #         file=video_file,
        #         response_format="text"
        #     )
        #     st.success("Transcription successful:")
        #     return transcript
        # except openai.APIError as e:
        #     if (("size limit" in str(e)) | ("Error code: 413" in str(e))):
        #         st.warning("File size exceeds the API limit. Attempting to split the file...")

                #Check video_file type
                if ".mp4" in video_file.name:
                    cmd = 'find / -iname ' + ''.join(video_file.name) + ' -print -quit 2>/dev/null'
                    
                    # command = 'ls'
                    #result = subprocess.call("find / -iname ", + ''.join(video_file.name), + " -print -quit 2>/dev/null", shell=True)
                    # Run the command and capture the output
                    find_file = subprocess.run(cmd, capture_output=True, text=True, shell=True)

                    # Access the output, return code, and other attributes
                    file_path = find_file.stdout
                    error_output = find_file.stderr
                    return_code = find_file.returncode
                    print(file_path)
                    st.write(file_path)

                    # output_file_path = file_path[:-3] + 'wav'
                    # print(output_file_path)
                    # st.write(output_file_path)
                    # cmd1 = "ffmpeg -i " + file_path + " -ab 160k -ac 2 -ar 44100 -vn " + output_file_path
                    # convert_file = subprocess.call("cd ..", shell=True)

                    # st.write(convert_file)
                    st.success("Success")

                # # Read the content of the file
                # file_content = video_file.read()

                # # PyDub handles time in milliseconds
                # ten_minutes = 10 * 60 * 1000
                # first_10_minutes = file_content[:ten_minutes]

if st.button('Transcribe and Analyze Videos'):
    transcript = transcribe(video_file)
    st.markdown(transcript)