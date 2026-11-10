from __future__ import annotations

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    """Optional local sentence-embedding model (pip install agentdup[embed]). No API calls."""

    def __init__(self, model: str = DEFAULT_MODEL, device: str = "cpu", max_chars: int = 2000):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model, device=device)
        self.max_chars = max_chars
        self._cache: dict[str, list] = {}

    def encode(self, texts: list[str]):
        todo = [t for t in dict.fromkeys(texts) if t not in self._cache]
        if todo:
            vecs = self.model.encode(
                [t[: self.max_chars] for t in todo],
                batch_size=64,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            self._cache.update(zip(todo, vecs))
        return [self._cache[t] for t in texts]
