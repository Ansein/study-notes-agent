# main.py
import sys
from pathlib import Path
from study_agent_core import StudyAgent
from modules.embedding_index import semantic_search
from modules.card_manager import get_random_card
from modules.persona_manager import detect_subject

# 初始化智能体
def load_agent():
    return StudyAgent()

agent = load_agent()

def get_recent_notes(n=5):
    notes_dir = Path("data/notes")
    if not notes_dir.exists():
        return []
    paths = sorted(notes_dir.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    return [p for p in paths[:n]]

def main():
    print("🎓 Study Notes Agent v1 — 学习笔记智能体（CLI版）")
    print("随行私人专家 · 自动笔记生成 · 可搜索 · 可复习\n")

    while True:
        print("\n🧭 导航与状态")
        print("1. 📘 学习模式")
        print("2. 🔍 搜索笔记")
        print("3. 📖 复习模式")
        print("4. 查看最近笔记")
        print("5. 退出")
        choice = input("选择功能模式 (1-5): ").strip()

        if choice == '1':  # 学习模式子循环
            print("\n📘 学习模式（输入 'q' 退出回主菜单）")
            print("输入概念或问题，智能体会以合适人格回答并自动保存笔记。")
            last_subject = None
            while True:
                user_input = input("请输入你的问题（输入 'q' 退出）: ").strip()
                if user_input.lower() == 'q':
                    break
                if user_input:
                    print("思考中...")
                    subject = detect_subject(user_input)
                    if subject == "default" and last_subject:
                        subject = last_subject
                    answer, note_path = agent.handle_query(user_input, subject=subject)
                    print(f"**识别学科：** {subject}")
                    print("\n---")
                    print("### 💡 回答")
                    print(answer)
                    if note_path:
                        print(f"✅ 已保存笔记到：{note_path}")
                    last_subject = subject
                else:
                    print("请输入问题。")

        elif choice == '2':  # 搜索模式子循环
            print("\n🔍 搜索模式（输入 'q' 退出回主菜单）")
            while True:
                query = input("输入关键词或自然语言查询: ").strip()
                if query.lower() == 'q':
                    break
                if query:
                    print("检索中...")
                    results = semantic_search(query)
                    print("### 检索结果")
                    print(results)
                else:
                    print("请输入搜索内容。")

        elif choice == '3':  # 复习模式子循环
            print("\n📖 复习模式（按 Enter 抽取一题，输入 'q' 退出回主菜单）")
            while True:
                prompt = input("").strip()
                if prompt.lower() == 'q':
                    break
                q, a = get_random_card()
                print(f"**Q：** {q}")
                print(f"**A：** {a}")

        elif choice == '4':  # 查看最近笔记（单次，立即返回）
            print("\n🗂️ 最近笔记")
            notes = get_recent_notes()
            if not notes:
                print("暂无笔记")
            else:
                for note in notes:
                    with open(note, "r", encoding="utf-8") as f:
                        preview = f.readline().strip().replace("#", "")
                    print(f"- {preview} ({note})")

        elif choice == '5':
            print(" goodbye!")
            sys.exit(0)

        else:
            print("无效选择，请重试。")

if __name__ == "__main__":
    main()
