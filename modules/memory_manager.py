# modules/memory_manager.py
import json
import os
from collections import deque

class MemoryManager:
    def __init__(self, max_items=3):
        self.max_items = max_items
        self.memory_dir = "data/memory"
        os.makedirs(self.memory_dir, exist_ok=True)

    def _file_path(self, subject):
        return os.path.join(self.memory_dir, f"{subject}.json")

    def load_recent(self, subject):
        path = self._file_path(subject)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
        return data[-self.max_items:]

    def update(self, subject, question, answer):
        path = self._file_path(subject)
        memory = self.load_recent(subject)
        memory.append({"question": question, "answer": answer})
        memory = deque(memory, maxlen=self.max_items)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(list(memory), f, ensure_ascii=False, indent=2)
