from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
import time
from proxy_manager import get_random_proxy
import streamlit as st
import os

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

    for attempt in range(max_retries):
        proxy = get_random_proxy()
        print("PROXY", proxy)
        print("PROXY", proxy.replace("http://", "").split("@")[-1].split(":"))
        proxy = proxy.replace("http://", "").split("@")[-1].split(":")
        host = proxy[0]
        port = proxy[1]

        try:
            print(f"Attempt {attempt+1} with proxy {proxy}")

            ytt_api = YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    # proxy_host=host,
                    # proxy_port=int(port),
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
        
        except Exception as e:
            print(f"Proxy failed (attempt {attempt+1}): {e}")
            time.sleep(2)

    raise Exception("All proxy attempts failed to fetch the transcript.")

def fetch_transcript_yt_dlp(video_url):
    import yt_dlp
    import pysrt

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "srt",
        "convertsubtitles": "srt",
        "outtmpl": "subtitles/%(id)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_id = info["id"]
        srt_file = f"{video_id}.en.srt"

    if not os.path.exists(srt_file):
        raise FileNotFoundError("❌ Subtitles not found. The video may not have captions in English.")

    subs = pysrt.open(srt_file)
    full_text = " ".join([sub.text for sub in subs])
    print(full_text)
    return full_text