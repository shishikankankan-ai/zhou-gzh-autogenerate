#!/usr/bin/env python3
"""微信公众号 API 公共工具：配置读取、token 缓存、上传、错误码翻译。

被 check_env.py 和 push_draft.py 共用。小白不需要关心这个文件，
只需要按 README 配好 .env 即可。

接口路径均来自微信开放文档（2026-11 核对）：
- token:            /cgi-bin/token
- 上传永久素材:      /cgi-bin/material/add_material
- 上传正文内图片:    /cgi-bin/media/uploadimg
- 新增草稿:          /cgi-bin/draft/add
- 草稿总数:          /cgi-bin/draft/count
"""
import json
import mimetypes
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

API_BASE = "https://api.weixin.qq.com"

# 常见错误码 → 人话。小白看到报错时直接给结论，不用自己猜。
ERR_HINT = {
    40001: "AppSecret 不对，去开发者平台重置一次，更新 .env",
    40013: "AppID 不对，检查 .env 里的 WECHAT_APPID",
    40005: "图片格式不对，封面只认 jpg/png",
    40009: "图片太大，正文内图片必须小于 1MB",
    40164: "IP 不在白名单。去公众平台『设置与开发-基本配置-IP白名单』加当前公网 IP（IPv4 和 IPv6 都加）",
    48001: "账号没有这个接口的权限。草稿接口一般都有；若报这个，改用手动复制到后台",
    45009: "接口调用太频繁，等一会儿再试",
}


def load_env():
    """读取 .env（不覆盖已有的真实环境变量）。"""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def get_credentials():
    """返回 (appid, secret)。缺失返回空串。"""
    load_env()
    return os.environ.get("WECHAT_APPID", ""), os.environ.get("WECHAT_SECRET", "")


def hint(errcode):
    """把错误码翻译成中文提示。"""
    return ERR_HINT.get(errcode, "以微信官方文档错误码为准")


def request_json(url, data=None, headers=None, timeout=30):
    """发 HTTPS 请求并解析 JSON。data 为 dict 时按 JSON 发送。"""
    if isinstance(data, dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers = {**(headers or {}), "Content-Type": "application/json"}
    else:
        body = data
    req = urllib.request.Request(url, data=body, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _cache_path():
    return Path(__file__).resolve().parent.parent / ".cache" / "wechat_token.json"


def get_token(appid, secret, use_cache=True):
    """拿 access_token，带本地缓存。token 有效期 7200 秒，提前 5 分钟刷新。"""
    if use_cache:
        cache = _cache_path()
        if cache.exists():
            try:
                saved = json.loads(cache.read_text(encoding="utf-8"))
                if (
                    saved.get("appid") == appid
                    and saved.get("expire_at", 0) > time.time() + 300
                ):
                    return saved["access_token"]
            except (ValueError, KeyError):
                pass

    url = (
        f"{API_BASE}/cgi-bin/token?grant_type=client_credential"
        f"&appid={urllib.parse.quote(appid)}&secret={urllib.parse.quote(secret)}"
    )
    data = request_json(url)
    token = data.get("access_token")
    if not token:
        code = data.get("errcode")
        raise RuntimeError(f"拿 token 失败（{code}）：{hint(code)}。原始返回：{data}")
    if use_cache:
        cache = _cache_path()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(
            json.dumps(
                {"appid": appid, "access_token": token, "expire_at": time.time() + 7200}
            ),
            encoding="utf-8",
        )
    return token


def upload_multipart(token, image_path, endpoint, extra_params=""):
    """通用的图片上传（multipart/form-data），返回解析后的 JSON。

    endpoint 分两种：
      material/add_material  → 封面，返回 media_id（永久素材）
      media/uploadimg        → 正文内图片，返回 url（微信域名）
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"找不到图片：{image_path}")
    suffix = path.suffix.lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}.get(
        suffix, mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    )
    boundary = "----" + uuid.uuid4().hex
    with open(path, "rb") as fh:
        payload = fh.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + payload + f"\r\n--{boundary}--\r\n".encode("utf-8")
    url = f"{API_BASE}{endpoint}?access_token={token}{extra_params}"
    return request_json(
        url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )


def check_result(data, need_key, what):
    """检查接口返回：有 errcode 非0 就报错，缺目标字段也报错。"""
    code = data.get("errcode", 0)
    if code != 0:
        raise RuntimeError(f"{what}失败（{code}）：{hint(code)}。原始返回：{data}")
    if need_key not in data:
        raise RuntimeError(f"{what}返回里没有 {need_key}，原始返回：{data}")
    return data[need_key]
