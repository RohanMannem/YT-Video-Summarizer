from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import streamlit as st

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

# def fetch_transcript_yt_dlp(video_url):
#     import yt_dlp
#     import pysrt

#     ydl_opts = {
#         "skip_download": True,
#         "writesubtitles": True,
#         "writeautomaticsub": True,
#         "subtitleslangs": ["en"],
#         "subtitlesformat": "srt",
#         "convertsubtitles": "srt",
#         "outtmpl": "subtitles/%(id)s.%(ext)s",
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(video_url, download=True)
#         video_id = info["id"]
#         srt_file = f"{video_id}.en.srt"

#     if not os.path.exists(srt_file):
#         raise FileNotFoundError("❌ Subtitles not found. The video may not have captions in English.")

#     subs = pysrt.open(srt_file)
#     full_text = " ".join([sub.text for sub in subs])
#     print(full_text)
#     return full_text