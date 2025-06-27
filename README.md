# 🎥 YouTube Video Summarizer

This Python-based tool takes a YouTube video ID, fetches the video transcript, and generates concise extractive summaries using two NLP approaches: one built with spaCy and the other with NLTK.

Compare their outputs side-by-side and understand how different NLP libraries handle text summarization.

---

## ✨ Features

- ✅ Fetches transcripts using the `youtube-transcript-api`
- ✅ Sentence tokenization and frequency-based extractive summarization using:
  - NLTK
  - spaCy (with Sentencizer)
- ✅ Clean CLI interface
- ✅ Modular and easy to extend (e.g., LLM-based summaries coming soon)

---

## 🚀 Usage

### 🔧 CLI Example

```bash
python summarizer.py --video_id dQw4w9WgXcQ
```

## Example Output
📜 spaCy Summary:
- Sentence 1...
- Sentence 2...

📜 NLTK Summary:
- Sentence 1...
- Sentence 2...

---

## 🛠️ Installation

Set up the project locally in just a few steps.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yt-summarizer.git
cd yt-summarizer
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Project Structure
```bash
yt-summarizer/
├── summarizer.py          # Main script for fetching and summarizing transcripts
├── utils.py               # Helper functions (optional)
├── requirements.txt       # Project dependencies
└── README.md              # You're reading this!
```
---

## 🧠 What I Learned

- Working with the YouTube Transcript API
- Text preprocessing and tokenization with NLTK and spaCy
- Frequency-based extractive summarization
- Structuring a simple but extensible NLP project
- Comparing multiple NLP modules to understand strengths and weaknesses

---

## 🔮 Future Improvements

- [ ] Add GPT-based abstractive summarization using OpenAI or Anthropic APIs
- [ ] Build a Streamlit or Gradio front-end for easy interaction
- [ ] Incorporate vector search and Q&A (Retrieval-Augmented Generation style)
- [ ] Integrate evaluation metrics (e.g., ROUGE, BLEU, human feedback)
- [ ] Log summary usage and feedback for fine-tuning or improvement
- [ ] Build in to a Chrome extension



