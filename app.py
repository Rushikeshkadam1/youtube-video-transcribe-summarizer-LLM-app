import streamlit as st
from dotenv import load_dotenv
load_dotenv() # to load all enviroment variables
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt='''You are a Youtube video summerizer. You will take transcript text and 
summarizing the entire video and providing important summary points within 300 words. please provide the summary of text geven here:
'''

# Getting Trnascripted data from YouTube videos
def extract_transcript_details(youtube_video_url, language="en-GB"):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        # Specify language code in the API request
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi", "en"])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        
        return transcript

    except Exception as e:
        raise e



# Getting summary based on prompt using Google Gemini pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text



st.title("YouTube Transcript to Detailed Note Converter")
youtube_link = st.text_input("Enter YouTube video link: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown('## Deatiled Notes:')
        st.write(summary)

