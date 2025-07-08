import spacy

nlp = spacy.load("en_core_web_sm")

def chunk_transcript(text, max_tokens=500, overlap=100):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    chunks = []
    i = 0

    while i < len(sentences):
        current_chunk = []
        current_len = 0
        chunk_start = i

        # Build a chunk up to max_tokens
        while i < len(sentences) and current_len < max_tokens:
            sentence = sentences[i]
            sent_len = len(nlp(sentence))
            if current_len + sent_len > max_tokens:
                break
            current_chunk.append(sentence)
            current_len += sent_len
            i += 1

        chunks.append(" ".join(current_chunk))

        if i >= len(sentences):  # End of transcript
            break

        # Backtrack to create overlap
        overlap_tokens = 0
        overlap_start = i - 1
        while overlap_start >= chunk_start and overlap_tokens < overlap:
            sentence = sentences[overlap_start]
            overlap_tokens += len(nlp(sentence))
            if overlap_tokens < overlap:
                overlap_start -= 1

        i = max(overlap_start + 1, chunk_start + 1) # Set i to where the overlap starts

    return chunks

def chunk_timestamped_transcript(captions, max_tokens=50, overlap=20):
    sentences = []
    for caption in captions:
        doc = nlp(caption["text"])
        for sent in doc.sents:
            if sent.text.strip():
                sentences.append({
                    "text": sent.text.strip(),
                    "start_time": caption["start_time"]  # Use caption's start_time
                })
    # print(sentences[0])
    for s in sentences:
        for k, v in s.items():
            print(s[k],len(s[k]))
    print("GAP")
    sentences = []
    for caption in captions:
        sentences.append({
            "text": caption["text"].strip(),
            "start_time": caption["start_time"]
        })
    # print(sentences[0])
    for s in sentences:
        for k, v in s.items():
            print(len(s[k]))
    chunks = []
    i = 0

    while i < len(sentences):
        current_chunk = []
        current_len = 0
        chunk_start_idx = i

        # Build a chunk up to max_tokens
        while i < len(sentences) and current_len < max_tokens:
            sentence = sentences[i]
            sent_len = len(nlp(sentence["text"]))
            if current_len + sent_len > max_tokens:
                break
            current_chunk.append(sentence)
            current_len += sent_len
            i += 1

        chunk_text = " ".join(s["text"] for s in current_chunk)
        chunk_start = current_chunk[0]["start_time"] if current_chunk else None

        chunks.append({
            "text": chunk_text,
            "start_time": chunk_start,
            "sentences": current_chunk
        })

        if i >= len(sentences):  # End of transcript
            break

        # Backtrack to create overlap
        overlap_tokens = 0
        overlap_start = i - 1
        while overlap_start >= chunk_start_idx and overlap_tokens < overlap:
            sentence = sentences[overlap_start]
            overlap_tokens += len(nlp(sentence["text"]))
            if overlap_tokens < overlap:
                overlap_start -= 1

        i = max(overlap_start + 1, chunk_start_idx + 1) # Set i to where the overlap starts

    return chunks
