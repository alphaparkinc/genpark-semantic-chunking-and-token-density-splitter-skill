"""MCP server for Semantic Chunking and Token Density Splitter."""
import sys
import json
from client import SemanticDocumentChunker


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "split_into_sentences",
                    "description": "Splits text into clean sentences respecting abbreviations and paragraph boundaries",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                        },
                        "required": ["text"],
                    },
                },
                {
                    "name": "chunk_by_semantic_density",
                    "description": "Chunks text into density-optimized segments with sliding sentence overlap for RAG indexing",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "target_chunk_chars": {"type": "integer", "default": 400},
                            "max_chunk_chars": {"type": "integer", "default": 700},
                            "overlap_sentences": {"type": "integer", "default": 1},
                        },
                        "required": ["text"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "split_into_sentences":
            res = SemanticDocumentChunker.split_into_sentences(args.get("text", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "chunk_by_semantic_density":
            res = SemanticDocumentChunker.chunk_by_semantic_density(
                text=args.get("text", ""),
                target_chunk_chars=int(args.get("target_chunk_chars", 400)),
                max_chunk_chars=int(args.get("max_chunk_chars", 700)),
                overlap_sentences=int(args.get("overlap_sentences", 1)),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
