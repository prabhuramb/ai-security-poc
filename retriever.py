"""
retriever.py

A deliberately simple, inspectable retrieval component. Given a user query,
it scores each document in knowledge_base/ by keyword overlap and returns the
top matches. This stands in for a production RAG retriever; the simplicity is
intentional so that every step of the pipeline in this proof-of-concept is
auditable rather than opaque.

Each returned document carries a visibility tag ("PUBLIC" or "CONFIDENTIAL")
parsed from its first line. The retriever itself does NOT enforce anything
based on that tag -- enforcement (or its absence) happens downstream in
target_app.py, which is the point: retrieval finds relevant content
regardless of sensitivity, and access control has to happen elsewhere.
"""

import os
import re
from pathlib import Path

KB_DIR = Path(__file__).parent / "knowledge_base"


def _load_documents():
    docs = []
    for path in sorted(KB_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        first_line = text.splitlines()[0] if text.splitlines() else ""
        visibility_match = re.search(r"VISIBILITY:\s*(\w+)", first_line)
        visibility = visibility_match.group(1) if visibility_match else "PUBLIC"
        docs.append({
            "filename": path.name,
            "visibility": visibility,
            "text": text,
        })
    return docs


STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "what", "when", "where", "who", "how", "why", "do", "does", "did",
    "of", "to", "in", "on", "for", "and", "or", "my", "me", "i", "you",
    "your", "can", "could", "would", "should", "will", "shall", "with",
    "at", "by", "as", "it", "this", "that", "these", "those",
}


def _score(query, doc_text):
    query_terms = set(re.findall(r"[a-z]+", query.lower())) - STOPWORDS
    doc_terms = set(re.findall(r"[a-z]+", doc_text.lower())) - STOPWORDS
    if not query_terms:
        return 0
    return len(query_terms & doc_terms)


def retrieve(query, top_k=2, force_include=None):
    """
    Returns the top_k documents most relevant to `query`, by keyword overlap.

    force_include: optional filename to guarantee is included in results,
    regardless of score. Used only to deterministically stage the indirect-
    injection test case (meeting_notes.md) so the POC's retrieval step is
    reproducible rather than dependent on incidental keyword overlap.
    """
    docs = _load_documents()
    scored_pairs = [(d, _score(query, d["text"])) for d in docs]
    # Drop zero-score documents: a real retriever should not pad results with
    # irrelevant content just to fill top_k. Without this, ties at score 0
    # can pull unrelated documents (including the injected one) into queries
    # that have nothing to do with them, which would contaminate the benign
    # control cases.
    relevant = sorted(
        (d for d, s in scored_pairs if s > 0),
        key=lambda d: _score(query, d["text"]),
        reverse=True,
    )

    if force_include:
        forced = [d for d in docs if d["filename"] == force_include]
        rest = [d for d in relevant if d["filename"] != force_include]
        result = (forced + rest)[:top_k]
    else:
        result = relevant[:top_k]

    return result


if __name__ == "__main__":
    # Quick manual check
    for r in retrieve("What is the vacation policy?"):
        print(r["filename"], r["visibility"])
