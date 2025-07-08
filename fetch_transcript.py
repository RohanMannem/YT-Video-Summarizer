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

def fetch_timestamped_sentences(video_id, max_sentence_length=100):
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
            # Split long sentence if needed before adding
            if len(current_sentence) > max_sentence_length:
                split_sentences = split_long_sentence(current_sentence, max_sentence_length)
                for i, split_sent in enumerate(split_sentences):
                    sentences.append({
                        "text": split_sent.strip(),
                        "start_time": format_seconds_to_hhmmss(current_start_time)
                    })
            else:
                sentences.append({
                    "text": current_sentence.strip(),
                    "start_time": format_seconds_to_hhmmss(current_start_time)
                })
            current_sentence = ""
            current_start_time = None
        # Force split if sentence gets too long (fallback)
        elif len(current_sentence) > max_sentence_length:
            # Find a good breaking point (prefer end of words)
            break_point = find_break_point(current_sentence, max_sentence_length)
            
            # Add the first part as a sentence
            sentences.append({
                "text": current_sentence[:break_point].strip(),
                "start_time": format_seconds_to_hhmmss(current_start_time)
            })
            
            # Keep the remainder for the next sentence
            remainder = current_sentence[break_point:].strip()
            if remainder:
                current_sentence = remainder
                # Keep the same start_time since we're continuing the same logical sentence
            else:
                current_sentence = ""
                current_start_time = None

    # Add any leftover text as a sentence if it doesn't end with punctuation
    if current_sentence:
        # Split if it's still too long
        if len(current_sentence) > max_sentence_length:
            split_sentences = split_long_sentence(current_sentence, max_sentence_length)
            for split_sent in split_sentences:
                sentences.append({
                    "text": split_sent.strip(),
                    "start_time": format_seconds_to_hhmmss(current_start_time)
                })
        else:
            sentences.append({
                "text": current_sentence.strip(),
                "start_time": format_seconds_to_hhmmss(current_start_time)
            })
    
    return sentences

def find_break_point(text, max_length):
    """Find a good breaking point in text, preferring word boundaries."""
    if len(text) <= max_length:
        return len(text)
    
    # Try to break at a word boundary near the max length
    # Look backwards from max_length to find a space
    for i in range(max_length, max(0, max_length - 50), -1):
        if text[i] == ' ':
            return i
    
    # If no good word boundary found, just break at max_length
    return max_length

def split_long_sentence(sentence, max_length):
    """Split a long sentence into multiple parts at word boundaries."""
    if len(sentence) <= max_length:
        return [sentence]
    
    parts = []
    remaining = sentence
    
    while len(remaining) > max_length:
        break_point = find_break_point(remaining, max_length)
        parts.append(remaining[:break_point])
        remaining = remaining[break_point:].strip()
    
    # Add the final part
    if remaining:
        parts.append(remaining)
    
    return parts