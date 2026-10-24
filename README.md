# genpark-semantic-chunking-and-token-density-splitter-skill

Sentence-boundary RAG document chunker, token density optimizer, and semantic topic transition splitter.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities

- **Grammar-Aware Sentence Boundary Splitting**: Accurately recognizes real sentence terminations while avoiding false splits on honorifics and abbreviations (`Dr.`, `e.g.`, `vs.`, `Inc.`).
- **Token Density Optimization**: Automatically balances chunk length between target and maximum character bounds for vector embedding models.
- **Sliding Sentence Overlap**: Preserves cross-boundary semantic context between adjacent chunks to maintain cohesion during vector retrieval.
- **Metadata Generation**: Calculates chunk indices, estimated tokens, character lengths, and sentence totals for vector database payload enrichment.

## Architecture

```
[Raw Markdown / Narrative Document Text]
                    │
                    ▼
┌─────────────────────────────────────────────────────┐
│             SemanticDocumentChunker                 │
│  - Abbreviation-Safe Sentence Boundary Tokenizer    │
│  - Target / Max Character Density Packer            │
│  - Sliding N-Sentence Overlap Window Manager        │
│  - Token Estimation & Chunk Metadata Enricher       │
└─────────────────────────────────────────────────────┘
                    │
                    ▼
[Density-Optimized Semantic Chunks + Overlap Payloads]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `split_into_sentences`: Splits text into clean sentences respecting abbreviations and paragraph boundaries.
- `chunk_by_semantic_density`: Chunks text into density-optimized segments with sliding sentence overlap for RAG indexing.

## Quickstart (Python API)

```python
from client import SemanticDocumentChunker

doc = "Enterprise AI requires accurate chunking. Dr. Lee proved this in 2024."
chunks = SemanticDocumentChunker.chunk_by_semantic_density(doc, target_chunk_chars=100)
print(f"Generated {len(chunks)} chunks.")
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
