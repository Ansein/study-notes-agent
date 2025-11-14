# modules/persona_manager.py
import json
import re
from pathlib import Path

PERSONA_PATH = Path("config/persona.json")

def load_persona():
    if PERSONA_PATH.exists():
        return json.load(open(PERSONA_PATH, "r", encoding="utf-8"))
    else:
        # 默认人格模板
        return {
            "data_science": "你是数据科学专家，擅长机器学习、统计建模与Python实现。回答时要精准、逻辑清晰。",
            "economics": "你是经济学家，熟悉微观、宏观与计量经济学理论，回答时应兼顾直觉与公式。",
            "ai": "你是人工智能专家，精通深度学习、神经网络与模型原理，回答应系统且简洁。",
            "computer_science": "你是计算机科学专家，擅长算法、数据结构、编程语言和系统设计。回答时要精确、结构化。",
            "default": "你是专业学者型助手，专注于知识性回答，避免泛化或闲聊。"
        }

def detect_subject(text: str):
    """
    基于关键词匹配的轻量学科识别
    """
    text = text.lower()
    patterns = {
        "data_science": r"(数据科学|machine learning|统计|回归|优化算法|机器学习|数据分析|数据挖掘|数据可视化)",
        "economics": r"(经济|价格|均衡|效用|市场|宏观|微观|财政|博弈|应用经济学|计量经济学)",
        "ai": r"(ai|人工智能|神经网络|深度学习|大模型|transformer|nlp|llm)",
        "computer_science": r"(计算机科学|数据结构|C语言|C++|Java|Python|操作系统|网络|数据库|系统设计|软件工程|计算机网络)"
    }
    for subj, pattern in patterns.items():
        if re.search(pattern, text):
            return subj
    return "default"
