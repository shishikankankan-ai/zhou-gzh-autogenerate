#!/usr/bin/env python3
"""把排版好的文章推进公众号草稿箱（不群发）。

前置：先跑 python scripts/check_env.py 三项全绿。
用法：
    python scripts/push_draft.py --html output/article.html \
        --cover output/cover.jpg --title "标题"

小白一次成功的保证（这些坑脚本都替你处理了）：
- 标题超 32 字 → 直接拦下并提示（微信官方限制）
- 正文里的本地图片 → 自动上传到微信换成合法 URL（外链图会被微信过滤）
- 封面 → 自动按 jpg/png 上传为永久素材
- token → 自动缓存，2 小时内复用，不用反复获取
- 报错 → 翻译成中文提示，直接告诉你怎么修

最后一步"发布"不在这个脚本里，必须去公众号后台人工点。
"""
import argparse
import re
import sys
from pathlib import Path

from wx_api import (
    check_result,
    get_credentials,
    get_token,
    request_json,
    upload_multipart,
    API_BASE,
)

IMG_TAG = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
DATA_URI = re.compile(r"^data:image/[^;]+;base64,(.+)$", re.DOTALL)


def body_char_count(text):
    """按微信口径数字符：中文算1个字，英文数字也算1个。"""
    return len(text)


def prepare_content(html_text, token, base_dir):
    """把正文里的图片换成微信域名 URL。

    处理三种图片：
    1. 本地路径 / 相对路径 → 上传后换成微信 URL
    2. base64 内嵌图      → 解码上传后换成微信 URL
    3. 已经是微信域名      → 保留
    4. 其他外链            → 保留但警告（微信会过滤掉）
    """
    warnings = []

    def replace(match):
        src = match.group(1)
        if "mmbiz.qpic.cn" in src or src.startswith("https://mmbiz"):
            return match.group(0)
        data_uri = DATA_URI.match(src)
        if data_uri:
            import base64

            raw = base64.b64decode(data_uri.group(1))
            tmp = base_dir / ".cache" / f"inline_{abs(hash(src))}.png"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_bytes(raw)
            local_path = tmp
        elif src.startswith(("http://", "https://")):
            warnings.append(f"外链图片会被微信过滤，请换成正文内上传：{src[:60]}...")
            return match.group(0)
        else:
            local_path = (base_dir / src).resolve()
            if not local_path.exists():
                warnings.append(f"找不到图片，微信会忽略：{src}")
                return match.group(0)

        resp = upload_multipart(token, str(local_path), "/cgi-bin/media/uploadimg")
        url = check_result(resp, "url", "上传正文图片")
        return match.group(0).replace(src, url)

    return IMG_TAG.sub(replace, html_text), warnings


def main():
    parser = argparse.ArgumentParser(description="把文章推进公众号草稿箱（不群发）")
    parser.add_argument("--html", required=True, help="排版好的 HTML 文件路径")
    parser.add_argument("--cover", required=True, help="封面图片路径（jpg/png）")
    parser.add_argument("--title", required=True, help="标题（≤32 字）")
    parser.add_argument("--author", default="", help="作者（≤16 字）")
    parser.add_argument("--digest", default="", help="摘要（≤120 字，留空自动抓正文前54字）")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent

    title_len = body_char_count(args.title)
    if title_len > 32:
        print(f"标题 {title_len} 字，超过微信 32 字上限，请先缩短。")
        return 1
    if body_char_count(args.author) > 16:
        print("作者超过 16 字上限，请先缩短。")
        return 1
    if body_char_count(args.digest) > 120:
        print("摘要超过 120 字上限，请先缩短。")
        return 1

    appid, secret = get_credentials()
    if not appid or not secret:
        print("没配 WECHAT_APPID / WECHAT_SECRET，先复制 .env.example 成 .env 并填写。")
        return 1

    html_path = Path(args.html)
    if not html_path.is_absolute():
        html_path = (Path.cwd() / html_path).resolve()
    cover_path = Path(args.cover)
    if not cover_path.is_absolute():
        cover_path = (Path.cwd() / cover_path).resolve()
    if not html_path.exists():
        print(f"找不到 HTML 文件：{html_path}")
        return 1
    if not cover_path.exists():
        print(f"找不到封面图片：{cover_path}")
        return 1

    try:
        token = get_token(appid, secret)

        print("上传封面...")
        cover_resp = upload_multipart(token, str(cover_path), "/cgi-bin/material/add_material", "&type=image")
        thumb_id = check_result(cover_resp, "media_id", "上传封面")

        print("处理正文图片...")
        content = html_path.read_text(encoding="utf-8")
        content, warnings = prepare_content(content, token, base_dir)
        for w in warnings:
            print(f"  提醒：{w}")

        article = {
            "article_type": "news",
            "title": args.title,
            "author": args.author,
            "digest": args.digest,
            "content": content,
            "thumb_media_id": thumb_id,
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
        }
        print("创建草稿...")
        resp = request_json(f"{API_BASE}/cgi-bin/draft/add?access_token={token}", data={"articles": [article]})
        media_id = check_result(resp, "media_id", "创建草稿")

        print(f"\n草稿创建成功，media_id：{media_id}")
        print("去公众号后台『草稿箱』检查排版和封面，确认后人工点发布。")
        return 0
    except Exception as exc:
        print(f"\n失败：{exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
