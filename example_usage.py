"""Example usage for Semantic Chunking and Token Density Splitter."""
from client import SemanticDocumentChunker


def main():
    sample_text = (
        "Modern enterprise AI applications require clean RAG chunking. "
        "Dr. Smith demonstrated that naive token window slicing cuts words in half (e.g., in the middle of sentences). "
        "Semantic chunking respects grammatical boundaries. "
        "Furthermore, by preserving a sliding sentence overlap, neighboring chunks retain context across transitions.\n\n"
        "In production benchmarks, this approach improved context retrieval precision by 27%. "
        "It also eliminated broken code blocks and fragmented JSON payloads. "
        "The GenPark ecosystem adopts 100% Python Standard Library implementations for all indexing operations."
    )

    print("=== 1. Clean Sentence Splitting (Handling Dr. and e.g.) ===")
    sentences = SemanticDocumentChunker.split_into_sentences(sample_text)
    print(f"Total Sentences Extracted: {len(sentences)}")
    for i, s in enumerate(sentences):
        print(f"  [{i+1}] {s}")

    print("\n=== 2. Density-Aware Semantic Chunking with Overlap ===")
    chunks = SemanticDocumentChunker.chunk_by_semantic_density(
        sample_text,
        target_chunk_chars=250,
        max_chunk_chars=450,
        overlap_sentences=1,
    )
    print(f"Generated {len(chunks)} chunks:")
    for c in chunks:
        print(f"\n--- Chunk #{c['chunk_index']} ({c['character_count']} chars, ~{c['estimated_tokens']} tokens, {c['sentence_count']} sentences) ---")
        print(c["content"])


if __name__ == "__main__":
    main()
