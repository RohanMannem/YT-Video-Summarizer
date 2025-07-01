from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import YouTubeRequestFailed
import requests
import time
from proxy_manager import get_random_proxy, get_proxy_pool
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

    for attempt in range(max_retries):
        proxy = get_random_proxy()
        proxy_url = get_random_proxy()
        host, port = proxy.replace("http://", "").split("@")[-1].split(":")

        try:
            print(f"Attempt {attempt+1} with proxy {proxy}")

            ytt_api = YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    proxy_host=host,
                    proxy_port=int(port),
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