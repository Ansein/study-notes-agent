# study_agent_core.py
import datetime
from modules.deepseek_api import query_deepseek
from modules.persona_manager import detect_subject, load_persona
from modules.note_manager import save_note
from modules.memory_manager import MemoryManager
from modules.card_manager import generate_card
from modules.embedding_index import update_embedding_index
from modules.template_loader import render_note_template

class StudyAgent:
    def __init__(self):
        self.memory = MemoryManager()
        self.personas = load_persona()

    def handle_query(self, user_input: str, subject: str = None):
        """
        核心主流程：
        1. 检测用户意图或学科
        2. 选择人格
        3. 查询DeepSeek
        4. 保存笔记 & 更新缓存 & 索引
        """
        # 特殊命令：用户询问智能体身份
        if user_input.strip() in ["你是谁", "你会干什么", "你能做什么"]:
            return self._introduce_agent()

        # 1. 学科检测
        if subject is None:
            subject = detect_subject(user_input)

        # 2. 加载人格prompt
        persona = self.personas.get(subject, self.personas["default"])

        # 3. 上下文缓存
        context = self.memory.load_recent(subject)

        # 4. 调用DeepSeek生成回答
        answer = query_deepseek(user_input, persona, context)

        # 5. Markdown格式化
        note_text = render_note_template(subject, user_input, answer)

        # 6. 保存笔记
        note_path = save_note(subject, note_text)

        # 7. 更新缓存
        self.memory.update(subject, user_input, answer)

        # 8. 生成复习卡片
        generate_card(subject, user_input, answer)

        # 9. 更新语义索引
        update_embedding_index(subject, note_text)

        return answer, note_path

    def _introduce_agent(self):
        intro = (
            "我是 Study Notes Agent —— 你的智能学习笔记助手。\n\n"
            "📘 我能做的事包括：\n"
            "1️⃣ 解答数据科学、经济学、人工智能等领域的概念问题；\n"
            "2️⃣ 自动生成结构化的 Markdown 学习笔记并分类保存；\n"
            "3️⃣ 记住你最近的提问以保持上下文一致性；\n"
            "4️⃣ 从笔记中自动生成复习卡片，帮助你巩固知识；\n"
            "5️⃣ 支持语义搜索，让你随时重温之前的笔记。\n\n"
            "简而言之，我是一个『随行私人专家 + 学习记录系统』。"
        )
        return intro, None
