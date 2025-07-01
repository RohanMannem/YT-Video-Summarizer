from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
import os

load_dotenv()
proxy_username = os.getenv("WEBSHARE_PROXY_USERNAME")
proxy_password = os.getenv("WEBSHARE_PROXY_PASSWORD")

def fetch_transcript(video_id, streamlit=False):
    if streamlit:
        ytt_api = YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=proxy_username,
                proxy_password=proxy_username,
            )
        )
    else:
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