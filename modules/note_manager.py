# modules/note_manager.py
import os
from datetime import datetime

def save_note(subject: str, note_text: str):
    """
    将Markdown笔记保存到本地，一天内的笔记追加到同一个文件。
    """
    base_dir = os.path.join("data", "notes", subject)
    os.makedirs(base_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}.md"
    file_path = os.path.join(base_dir, filename)
    # 如果文件存在，则追加；否则创建新文件
    mode = "a" if os.path.exists(file_path) else "w"
    with open(file_path, mode, encoding="utf-8") as f:
        if mode == "a":
            f.write("\n\n---\n\n")  # 分隔符
        f.write(note_text)
    return file_path
