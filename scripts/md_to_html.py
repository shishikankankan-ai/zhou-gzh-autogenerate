#!/usr/bin/env python3
"""把 Markdown 转成带内联样式的 HTML，供公众号编辑器粘贴。

只用提示词时不需要这个——03-layout 的提示词直接让 AI 出 HTML。
这个是给"想本地离线转换、不调用 AI"的人准备的备选。
用法：python scripts/md_to_html.py input.md > output/article.html

只处理常见 Markdown：标题、段落、加粗、列表。复杂语法请用提示词方式。
"""
import html
import re
import sys

BODY_STYLE = "font-size:16px;line-height:1.75;color:#333;"
H1_STYLE = "font-size:22px;font-weight:bold;margin:1em 0 0.6em;"
H2_STYLE = "font-size:18px;font-weight:bold;margin:1.5em 0 0.5em;"
H3_STYLE = "font-size:17px;font-weight:bold;margin:1.2em 0 0.4em;"


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def convert(md):
    out = []
    for raw in md.splitlines():
        line = raw.strip()
        if not line or (set(line) <= {"-", "*"} and len(line) >= 3):
            continue
        if line.startswith("# "):
            out.append(f'<h1 style="{H1_STYLE}">{inline(line[2:])}</h1>')
        elif line.startswith("## "):
            out.append(f'<h2 style="{H2_STYLE}">{inline(line[3:])}</h2>')
        elif line.startswith("### "):
            out.append(f'<h3 style="{H3_STYLE}">{inline(line[4:])}</h3>')
        elif line.startswith("- "):
            out.append(f'<p style="margin:0.3em 0;">• {inline(line[2:])}</p>')
        else:
            out.append(f'<p style="margin:0 0 1em;">{inline(line)}</p>')
    return f'<div style="{BODY_STYLE}">\n' + "\n".join(out) + "\n</div>"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python scripts/md_to_html.py input.md > output/article.html", file=sys.stderr)
        sys.exit(1)
    source = open(sys.argv[1], encoding="utf-8").read()
    print(convert(source))
