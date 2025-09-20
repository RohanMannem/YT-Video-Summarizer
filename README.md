# 🎥 YouTube Video Summarizer

This project summarizes YouTube videos by fetching their transcripts and generating concise summaries using both extractive NLP methods and LLMs. It's built with Streamlit and supports proxy-enabled transcript fetching, making it work even when YouTube blocks cloud apps.

Compare their outputs side-by-side and understand how different NLP libraries handle text summarization.

Demo: [streamlit-streamlit_app-2025-07-15-21-07-83.webm](https://github.com/user-attachments/assets/c0b4affd-adc3-4a59-b6a3-73922eacb340)

---

## ✨ Features

- ✅ Fetches transcripts using the `youtube-transcript-api`
- ✅ Sentence tokenization and frequency-based extractive summarization using NLTK and spaCy
- ✅ GPT-based summaries
- ✅ Streamlit UI for interactive usage
- ✅ CLI usage supported

---

## 🚀 Usage

### 🔧 CLI Example

```bash
python main.py --video_link "<youtube_url>"
```

## Example Output
📜 spaCy Summary:
```bash
in this new era of deep, consistent rosters where chemistry and fit matter just as much as talent, the okc thunder have built the youngest, most continuous roster in the entire league while being the best team in the league. but to say they have simply entered this club would actually be an understatement because throughout the 2025 season, the thunder finished with the sixth best record of all time, the second highest net rating of all time, and the largest margin of victory in the history of the league. among the championship teams in this era of parody, the 2020 lakers have had the lowest payroll, winning a title with just the 11th most expensive team in the league.
```

📜 NLTK Summary:
```bash
But to say they have simply entered this club would actually be an understatement because throughout the 2025 season, the Thunder finished with the sixth best record of all time, the second highest net rating of all time, and the largest margin of victory in the history of the league. In this new era of deep, consistent rosters where chemistry and fit matter just as much as talent, the OKC Thunder have built the youngest, most continuous roster in the entire league while being the best team in the league. Since 2019, the average roster continuity among championship teams, essentially how much a team stayed the same from one season to the next, was about 61%.
```

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
├── main.py                # Main script for fetching and summarizing transcripts
├── utils.py               # Helper functions (optional)
├── requirements.txt       # Project dependencies
└── README.md              # You're reading this!
```
---

## 🧠 What I Learned

- Working with the YouTube Transcript API
- Text preprocessing and tokenization with NLTK and spaCy
- Frequency-based extractive summarization
- Streamlit deployment
- Webshare proxy server configuration
- Using OpenAI API packages

---

## 🔮 Future Improvements

- [ ] Incorporate vector search and Q&A (Retrieval-Augmented Generation style)
- [ ] Integrate evaluation metrics (e.g., ROUGE, BLEU, human feedback)
- [ ] Log summary usage and feedback for fine-tuning or improvement
- [ ] Build in to a Chrome extension



