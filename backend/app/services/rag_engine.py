import os
from typing import List, Dict, Any, Optional
from app.config import settings

try:
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False


class RAGEngine:
    """
    Implements Contextual RAG with Semantic Chunking.
    Prepends situational contract metadata to each semantic chunk prior to embedding.
    """

    def __init__(self):
        self._memory_store: Dict[str, List[Dict[str, Any]]] = {}
        if HAS_CHROMADB:
            try:
                self.client = chromadb.PersistentClient(
                    path=settings.CHROMA_PERSIST_DIR,
                    settings=ChromaSettings(allow_reset=True, anonymized_telemetry=False)
                )
            except Exception:
                self.client = None
        else:
            self.client = None

    def get_or_create_collection(self, contract_id: str):
        if self.client:
            safe_name = f"contract_{contract_id.replace('-', '_')}"
            return self.client.get_or_create_collection(name=safe_name)
        return None

    def semantic_chunk_and_contextualize(
        self,
        contract_title: str,
        sections: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Creates semantic chunks and prepends contextual orientation to maximize retrieval accuracy.
        """
        contextual_chunks = []

        for sec in sections:
            sec_num = sec.get("section_number", "General")
            title = sec.get("title", "")
            raw_content = sec.get("content", "")
            page = sec.get("page_number", 1)

            # Split large sections into sub-chunks if longer than 1500 chars
            sub_chunks = []
            if len(raw_content) > 1500:
                paragraphs = raw_content.split("\n\n")
                curr = ""
                for p in paragraphs:
                    if len(curr) + len(p) < 1200:
                        curr += "\n\n" + p
                    else:
                        if curr.strip():
                            sub_chunks.append(curr.strip())
                        curr = p
                if curr.strip():
                    sub_chunks.append(curr.strip())
            else:
                sub_chunks = [raw_content] if raw_content.strip() else []

            for idx, chunk_text in enumerate(sub_chunks):
                # Contextual RAG: Prepend synthetic context prefix
                context_prefix = (
                    f"[Document: {contract_title} | Section: {sec_num} ({title}) | Page: {page}]\n"
                    f"Context: This excerpt defines terms and legal obligations governing {title.lower()}."
                )
                enriched_text = f"{context_prefix}\n\n{chunk_text}"

                contextual_chunks.append({
                    "id": f"{sec_num}_{idx}",
                    "text": enriched_text,
                    "raw_text": chunk_text,
                    "metadata": {
                        "contract_title": contract_title,
                        "section_number": sec_num,
                        "title": title,
                        "page_number": page,
                        "chunk_index": idx
                    }
                })

        return contextual_chunks

    def index_contract(self, contract_id: str, contract_title: str, sections: List[Dict[str, Any]]):
        """Indexes contextual chunks into ChromaDB or in-memory store."""
        chunks = self.semantic_chunk_and_contextualize(contract_title, sections)
        if not chunks:
            return

        self._memory_store[contract_id] = chunks

        collection = self.get_or_create_collection(contract_id)
        if collection:
            try:
                ids = [c["id"] for c in chunks]
                documents = [c["text"] for c in chunks]
                metadatas = [c["metadata"] for c in chunks]
                collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            except Exception:
                pass

    def query(self, contract_id: str, query_text: str, n_results: int = 4) -> List[Dict[str, Any]]:
        """Queries the contract index with hybrid semantic similarity."""
        try:
            collection = self.get_or_create_collection(contract_id)
            if collection:
                results = collection.query(
                    query_texts=[query_text],
                    n_results=min(n_results, max(1, collection.count()))
                )

                hits = []
                if results and results.get("documents") and len(results["documents"]) > 0:
                    docs = results["documents"][0]
                    metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                    ids = results["ids"][0] if results.get("ids") else [""] * len(docs)

                    for doc, meta, hit_id in zip(docs, metas, ids):
                        hits.append({
                            "id": hit_id,
                            "text": doc,
                            "metadata": meta
                        })
                return hits
            else:
                # In-memory keyword & relevance fallback
                chunks = self._memory_store.get(contract_id, [])
                tokens = set(query_text.lower().split())
                scored = []
                for c in chunks:
                    match_score = sum(1 for t in tokens if t in c["text"].lower())
                    scored.append((match_score, c))
                scored.sort(key=lambda x: x[0], reverse=True)
                return [{"id": c["id"], "text": c["text"], "metadata": c["metadata"]} for _, c in scored[:n_results]]
        except Exception:
            return []

    def delete_contract(self, contract_id: str):
        """Removes contract collection from ChromaDB and memory store."""
        self._memory_store.pop(contract_id, None)
        if self.client:
            safe_name = f"contract_{contract_id.replace('-', '_')}"
            try:
                self.client.delete_collection(name=safe_name)
            except Exception:
                pass


rag_engine = RAGEngine()
