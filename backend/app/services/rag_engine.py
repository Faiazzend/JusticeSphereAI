import math
import re
from typing import List, Dict, Any, Optional
from collections import Counter

from app.config import settings

try:
    import chromadb
except ImportError:
    chromadb = None


class RAGEngine:
    def __init__(self):
        self._memory_store: Dict[str, List[Dict[str, Any]]] = {}
        self.chroma_client = None

        if chromadb is not None:
            try:
                persist_path = str(settings.CHROMA_PERSIST_DIR)
                self.chroma_client = chromadb.PersistentClient(path=persist_path)
            except Exception:
                self.chroma_client = None

    def chunk_contract(
        self, contract_id: str, contract_title: str, sections: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Contextual Semantic Chunking:
        For each section, if length > 1500 chars, break into logical paragraphs.
        Prepends situational contextual header to every chunk.
        """
        chunks: List[Dict[str, Any]] = []
        chunk_idx = 0

        for sec in sections:
            sec_num = sec.get("section_number", "1")
            title = sec.get("title", "General Terms")
            page = sec.get("page_number", 1)
            content = sec.get("content", "")

            header = (
                f"[Document: {contract_title} | Section: {sec_num} ({title}) | Page: {page}]\n"
                f"Context: This excerpt defines terms and legal obligations governing {title.lower()}.\n"
            )

            # Sub-chunking if large
            if len(content) > 1500:
                paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                current_accum = []
                current_len = 0

                for para in paragraphs:
                    current_accum.append(para)
                    current_len += len(para)

                    if current_len >= 1200:
                        chunk_text = header + "\n" + "\n\n".join(current_accum)
                        chunks.append({
                            "chunk_id": f"{contract_id}_chunk_{chunk_idx}",
                            "text": chunk_text,
                            "metadata": {
                                "contract_id": contract_id,
                                "section_number": sec_num,
                                "title": title,
                                "page": page,
                            },
                        })
                        chunk_idx += 1
                        current_accum = []
                        current_len = 0

                if current_accum:
                    chunk_text = header + "\n" + "\n\n".join(current_accum)
                    chunks.append({
                        "chunk_id": f"{contract_id}_chunk_{chunk_idx}",
                        "text": chunk_text,
                        "metadata": {
                            "contract_id": contract_id,
                            "section_number": sec_num,
                            "title": title,
                            "page": page,
                        },
                    })
                    chunk_idx += 1
            else:
                chunk_text = header + "\n" + content
                chunks.append({
                    "chunk_id": f"{contract_id}_chunk_{chunk_idx}",
                    "text": chunk_text,
                    "metadata": {
                        "contract_id": contract_id,
                        "section_number": sec_num,
                        "title": title,
                        "page": page,
                    },
                })
                chunk_idx += 1

        # Cache in memory
        self._memory_store[contract_id] = chunks

        # Upsert into ChromaDB if available
        if self.chroma_client:
            try:
                coll_name = f"contract_{contract_id.replace('-', '_')}"
                collection = self.chroma_client.get_or_create_collection(name=coll_name)
                if chunks:
                    collection.upsert(
                        ids=[c["chunk_id"] for c in chunks],
                        documents=[c["text"] for c in chunks],
                        metadatas=[c["metadata"] for c in chunks],
                    )
            except Exception:
                pass

        return chunks

    def _term_frequency_similarity(self, query: str, chunks: List[Dict[str, Any]], n_results: int) -> List[Dict[str, Any]]:
        """Fallback in-memory token-frequency cosine scorer."""
        def tokenize(text: str) -> List[str]:
            return [w for w in re.findall(r"\w+", text.lower()) if len(w) > 2]

        query_tokens = tokenize(query)
        if not query_tokens:
            return chunks[:n_results]

        query_counts = Counter(query_tokens)
        query_norm = math.sqrt(sum(c * c for c in query_counts.values()))

        scored_chunks = []
        for ch in chunks:
            text = ch.get("text", "")
            doc_tokens = tokenize(text)
            doc_counts = Counter(doc_tokens)
            doc_norm = math.sqrt(sum(c * c for c in doc_counts.values()))

            if query_norm == 0 or doc_norm == 0:
                score = 0.0
            else:
                dot_product = sum(query_counts[t] * doc_counts.get(t, 0) for t in query_counts)
                score = dot_product / (query_norm * doc_norm)

            scored_chunks.append((score, ch))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [ch for _, ch in scored_chunks[:n_results]]

    def query(self, contract_id: str, query_text: str, n_results: int = 4) -> List[Dict[str, Any]]:
        """
        Query for relevant chunks using ChromaDB if possible,
        falling back to in-memory TF scorer.
        """
        if self.chroma_client:
            try:
                coll_name = f"contract_{contract_id.replace('-', '_')}"
                collection = self.chroma_client.get_collection(name=coll_name)
                results = collection.query(query_texts=[query_text], n_results=n_results)
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]
                ids = results.get("ids", [[]])[0]

                if docs:
                    return [
                        {"chunk_id": ids[i], "text": docs[i], "metadata": metas[i]}
                        for i in range(len(docs))
                    ]
            except Exception:
                pass

        chunks = self._memory_store.get(contract_id, [])
        return self._term_frequency_similarity(query_text, chunks, n_results)

    def delete_contract(self, contract_id: str) -> None:
        """Purge collections from ChromaDB and memory cache."""
        self._memory_store.pop(contract_id, None)

        if self.chroma_client:
            try:
                coll_name = f"contract_{contract_id.replace('-', '_')}"
                self.chroma_client.delete_collection(name=coll_name)
            except Exception:
                pass


rag_engine = RAGEngine()
