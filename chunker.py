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
        start_i = i  # Save starting index

        # Build a chunk up to max_tokens
        while i < len(sentences) and current_len < max_tokens:
            print(i, len(sentences))
            print(current_len, max_tokens)
            sentence = sentences[i]
            sent_len = len(nlp(sentence))
            if current_len + sent_len > max_tokens:
                break
            current_chunk.append(sentence)
            current_len += sent_len
            i += 1

        chunks.append(" ".join(current_chunk))
        print(current_chunk)

        if i >= len(sentences):  # End of transcript
            break

        # Backtrack to create overlap
        overlap_tokens = 0
        j = i - 1
        while j >= 0 and overlap_tokens < overlap:
            sentence = sentences[j]
            overlap_tokens += len(nlp(sentence))
            j -= 1
        i = j + 1  # Set i to where the overlap starts

    return chunks
