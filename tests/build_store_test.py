import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RAG.build_store import build_store
import sys
from datetime import datetime
from utils.extract_video_id import extract_video_id

current_datetime = datetime.now()
url = sys.argv[1] if len(sys.argv) > 1 else input("YouTube URL: ")
video_id = extract_video_id(url)
build_store(video_id, "vector_store/" + str(video_id))
