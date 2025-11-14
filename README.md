# Study Notes Agent

## 概述

内测版！

这是一个学习笔记智能体（Study Notes Agent），旨在帮助用户通过CLI界面学习各种学科知识。它使用DeepSeek API生成智能回答，并自动保存结构化的Markdown笔记。支持语义搜索、复习卡片和上下文记忆。

主要功能：
- **学习模式**：输入问题，智能体以合适的人格（例如数据科学专家）回答，并保存笔记。
- **搜索模式**：使用语义搜索查找现有笔记。
- **复习模式**：随机抽取复习卡片。
- **查看最近笔记**：列出最近生成的笔记。

## 安装

1. 克隆仓库：
   ```
   git clone https://github.com/Ansein/study-notes-agent.git
   cd 学习助手agent
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

注意：项目使用DeepSeek API，需要在项目根目录的.env文件设置 DEEPSEEK_API_KEY=您的API密钥。

## 使用

运行主程序：
```
python main.py
```

- 笔记保存在`data/notes/`目录下，按学科分类。
- 复习卡片保存在`data/cards/`目录下。