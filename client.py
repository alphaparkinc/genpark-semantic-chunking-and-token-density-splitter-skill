"""Semantic Chunking and Token Density Splitter.
100% Python Standard Library.
"""

import re
from typing import List, Dict, Any, Optional


class SemanticDocumentChunker:
    """Chunks documents for RAG grounding along natural sentence and paragraph boundaries,
    maintaining target token/character density and sentence-level semantic overlap."""

    KNOWN_ABBREVIATIONS = {
        "dr.", "mr.", "mrs.", "ms.", "prof.", "e.g.", "i.e.", "etc.", "vs.", "inc.", "ltd.", "co.", "dept.", "no."
    }

    @classmethod
    def split_into_sentences(cls, text: str) -> List[str]:
        """Splits narrative into clean standalone sentences, respecting abbreviations and ellipses."""
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        all_sentences = []

        # Find potential sentence ends: punctuation followed by space
        candidate_pattern = re.compile(r'([.!?]+)\s+')

        for para in paragraphs:
            start = 0
            for match in candidate_pattern.finditer(para):
                end_pos = match.end()
                preceding_text = para[start:match.start() + len(match.group(1))].strip()
                words = preceding_text.split()
                if words:
                    last_word = words[-1].lower()
                    # If last word is an abbreviation, do not split
                    if last_word in cls.KNOWN_ABBREVIATIONS:
                        continue

                # Valid sentence boundary
                sentence = para[start:match.end()].strip()
                if sentence:
                    all_sentences.append(sentence)
                start = end_pos

            remainder = para[start:].strip()
            if remainder:
                all_sentences.append(remainder)

        return all_sentences

    @classmethod
    def chunk_by_semantic_density(
        cls,
        text: str,
        target_chunk_chars: int = 400,
        max_chunk_chars: int = 700,
        overlap_sentences: int = 1,
    ) -> List[Dict[str, Any]]:
        """Packs sentences into coherent chunks respecting character limits and sliding sentence overlap."""
        sentences = cls.split_into_sentences(text)
        if not sentences:
            return []

        chunks = []
        i = 0
        total_s = len(sentences)

        while i < total_s:
            current_chunk_sentences = []
            current_length = 0

            # Accumulate sentences up to target length
            j = i
            while j < total_s:
                sent = sentences[j]
                sent_len = len(sent)

                if current_chunk_sentences and (current_length + sent_len) > max_chunk_chars:
                    break

                current_chunk_sentences.append(sent)
                current_length += sent_len + 1  # 1 for space
                j += 1

                if current_length >= target_chunk_chars:
                    break

            chunk_text = " ".join(current_chunk_sentences)
            words = chunk_text.split()
            # Estimate ~1.3 tokens per word
            est_tokens = int(len(words) * 1.3)

            chunks.append({
                "chunk_index": len(chunks),
                "sentence_count": len(current_chunk_sentences),
                "character_count": len(chunk_text),
                "word_count": len(words),
                "estimated_tokens": est_tokens,
                "content": chunk_text,
            })

            # Advance window with overlap
            advance = max(1, len(current_chunk_sentences) - overlap_sentences)
            i += advance

        return chunks
