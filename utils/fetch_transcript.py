from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import streamlit as st
from datetime import timedelta
import regex as re

def fetch_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)

    captions = []

    for snippet in fetched_transcript:
        captions.append(snippet.text)

    # indexable
    last_snippet = fetched_transcript[-1]

    # provides a length
    snippet_count = len(fetched_transcript)

    caption = ' '.join(captions)
    return caption

def proxy_fetch_transcript(video_id, max_retries=3):
    proxy_user = st.secrets["WEBSHARE_PROXY_USERNAME"]
    proxy_pass = st.secrets["WEBSHARE_PROXY_PASSWORD"]

    ytt_api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=proxy_user,
            proxy_password=proxy_pass,
        )
    )
    fetched_transcript = ytt_api.fetch(video_id)

    captions = []

    for snippet in fetched_transcript:
        captions.append(snippet.text)

    caption = ' '.join(captions)
    return caption

def format_seconds_to_hhmmss(seconds):
    return str(timedelta(seconds=int(seconds)))  # e.g., '0:01:12'

def fetch_timestamped_sentences(video_id):
    ytt_api = YouTubeTranscriptApi()
    raw_segments = ytt_api.get_transcript(video_id)

    sentences = []
    current_sentence = ""
    current_start_time = None

    for seg in raw_segments:
        text = seg["text"].strip().replace("\n", " ")
        if not text:
            continue

        if current_sentence == "":
            current_start_time = seg["start"]

        current_sentence += (" " if current_sentence else "") + text

        # Check if this segment ends with sentence-ending punctuation
        if re.search(r"[.!?]\"?$", text):
            sentences.append({
                "text": current_sentence.strip(),
                "start_time": format_seconds_to_hhmmss(current_start_time)
            })
            current_sentence = ""
            current_start_time = None

    # Add any leftover text as a sentence if it doesn't end with punctuation
    if current_sentence:
        sentences.append({
            "text": current_sentence.strip(),
            "start_time": format_seconds_to_hhmmss(current_start_time)
        })

    return sentences