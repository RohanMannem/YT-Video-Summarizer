import spacy

nlp = spacy.load("en_core_web_sm")

def chunk_transcript(text, max_tokens=500, overlap=100):
    """
    Splits transcript into overlapping chunks using spaCy sentence boundaries.

    Args:
        text (str): The full transcript.
        max_tokens (int): Max tokens per chunk.
        overlap (int): Number of tokens to overlap between chunks.

    Returns:
        List of strings (each chunk).
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    chunks = []
    current_chunk = []
    current_len = 0

    print(text)

    print()
    print(sentences)

    i = 0
    while i < len(sentences):
        print(f"Chunking sentence {i}/{len(sentences)}")
        print(sentences[i])
        while i < len(sentences) and current_len < max_tokens:
            sentence = sentences[i]
            sent_len = len(nlp(sentence))  # Count tokens via spaCy
            current_chunk.append(sentence)
            current_len += sent_len
            i += 1

        chunks.append(" ".join(current_chunk))

        print("ESCAPE")

        # Roll back index for overlap
        if overlap > 0:
            overlap_tokens = 0
            j = i - 1
            current_chunk = []
            while j >= 0 and overlap_tokens < overlap:
                sentence = sentences[j]
                sent_len = len(nlp(sentence))
                current_chunk.insert(0, sentence)
                overlap_tokens += sent_len
                j -= 1
        else:
            current_chunk = []

        current_len = sum(len(nlp(sent)) for sent in current_chunk)

    return chunks
