# modules/template_loader.py
from datetime import datetime
from jinja2 import Template

DEFAULT_TEMPLATE = """
# {{ title }}

**提问：** {{ question }}

**解答：**
{{ answer }}

> 学科：{{ subject }}
> 日期：{{ date }}
"""

def render_note_template(subject: str, question: str, answer: str):
    title = question.strip().replace("？", "").replace("?", "")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    template = Template(DEFAULT_TEMPLATE)
    note = template.render(
        title=title, question=question, answer=answer, subject=subject, date=date
    )
    return note
