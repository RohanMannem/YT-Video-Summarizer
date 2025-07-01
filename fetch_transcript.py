from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._api import _TranscriptApi
from youtube_transcript_api._errors import YouTubeRequestFailed
import requests
import time
from proxy_manager import get_random_proxy

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
    for attempt in range(max_retries):
        try:
            proxy_url = get_random_proxy()

            print(f"🔁 Attempt {attempt+1} using proxy: {proxy_url}")

            # Set up a proxy session
            session = requests.Session()
            session.proxies = {
                "http": proxy_url,
                "https": proxy_url,
            }

            # Fetch transcript with custom session
            transcript = _TranscriptApi._get_transcript(video_id, session=session)
            return transcript

        except YouTubeRequestFailed as e:
            print(f"Proxy failed (attempt {attempt+1}): {e}")
            time.sleep(2)  # small backoff
            continue
        except Exception as e:
            print(f"Unexpected error (attempt {attempt+1}): {e}")
            time.sleep(2)
            continue

    raise Exception("All proxy attempts failed to fetch the transcript.")