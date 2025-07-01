import streamlit as st
from fetch_transcript import fetch_transcript
from basic_summarizer import spacy_summarizer
from basic_summarizer import nltk_summarizer
from openai_summarizer import openai_summarizer

st.set_page_config(page_title="🎥 YouTube Video Summarizer", layout="centered")

st.title("🎥 YouTube Video Summarizer")
st.markdown("Fetch a YouTube video transcript and generate summaries using spaCy, NLTK, and GPT.")

video_id = st.text_input("Enter YouTube Video ID:", help="Only the video ID, not the full URL")

use_gpt = st.checkbox("Use GPT-4o Summary", value=False)
gpt_style = st.selectbox("GPT Summary Style", ["Default", "Bullets", "Explain Like I'm 5", "Short Paragraph"]) if use_gpt else None

if st.button("Summarize") and video_id:
    with st.spinner("Fetching transcript..."):
        transcript = fetch_transcript(video_id)

    if not transcript:
        st.error("❌ Could not fetch transcript. Check if the video has captions.")
    else:
        st.subheader("📜 Transcript Preview")
        st.text(transcript[:1000] + "..." if len(transcript) > 1000 else transcript)

        st.subheader("🧠 spaCy Summary")
        spacy_summary = spacy_summarizer(transcript)
        st.markdown(spacy_summary)

        st.subheader("🧪 NLTK Summary")
        nltk_summary = nltk_summarizer(transcript)
        st.markdown(nltk_summary)

        if use_gpt:
            st.subheader("🤖 GPT-4o Summary")
            prompt_styles = {
                "Default": f"Summarize this YouTube transcript:\\n\\n{transcript}",
                "Bullets": f"Summarize this transcript as 5–7 clear bullet points:\\n\\n{transcript}",
                "Explain Like I'm 5": f"Explain this video simply, like I'm 5 years old:\\n\\n{transcript}",
                "Short Paragraph": f"Summarize this transcript in 1 short paragraph:\\n\\n{transcript}",
            }
            gpt_summary = openai_summarizer(prompt_styles[gpt_style])
            st.markdown(gpt_summary)