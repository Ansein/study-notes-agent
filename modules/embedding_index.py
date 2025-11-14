# modules/embedding_index.py
import os
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_DIR = "data/embeddings"
os.makedirs(INDEX_DIR, exist_ok=True)

def _index_path(subject):
    return os.path.join(INDEX_DIR, f"{subject}.faiss")

def _meta_path(subject):
    return os.path.join(INDEX_DIR, f"{subject}_meta.json")

def update_embedding_index(subject, note_text):
    vec = MODEL.encode([note_text])
    index_path = _index_path(subject)
    meta_path = _meta_path(subject)

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        metas = json.load(open(meta_path, "r", encoding="utf-8"))
    else:
        index = faiss.IndexFlatL2(vec.shape[1])
        metas = []

    index.add(vec)
    metas.append(note_text[:200])  # 存储摘要
    faiss.write_index(index, index_path)
    json.dump(metas, open(meta_path, "w", encoding="utf-8"), ensure_ascii=False)

def semantic_search(query, top_k=3):
    vec = MODEL.encode([query])
    results = []
    for file in os.listdir(INDEX_DIR):
        if file.endswith(".faiss"):
            subject = file.replace(".faiss", "")
            index_path = _index_path(subject)
            meta_path = _meta_path(subject)
            index = faiss.read_index(index_path)
            metas = json.load(open(meta_path, "r", encoding="utf-8"))
            D, I = index.search(vec, top_k)
            for i, idx in enumerate(I[0]):
                if idx < len(metas):
                    results.append((subject, metas[idx], D[0][i]))
    results.sort(key=lambda x: x[2])
    output = "\n\n".join([f"### [{s}] {m}" for s, m, _ in results])
    return output if output else "未找到相关笔记"
