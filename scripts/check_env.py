#!/usr/bin/env python3
"""环境自检：验证配置、token、草稿接口权限三项，报错给中文提示。

只用提示词不需要跑这个。仅在用 scripts/push_draft.py 前运行：
    python scripts/check_env.py
"""
import sys

from wx_api import API_BASE, check_result, get_credentials, get_token, request_json


def main():
    appid, secret = get_credentials()
    ok = True

    print("[1/3] 环境变量")
    if appid and secret:
        print("  PASS  WECHAT_APPID / WECHAT_SECRET 已配置")
    else:
        print("  FAIL  没配 WECHAT_APPID 或 WECHAT_SECRET")
        print("        把 .env.example 复制成 .env，填入 AppID 和 AppSecret")
        return 1

    print("[2/3] access_token")
    try:
        get_token(appid, secret, use_cache=False)
        print("  PASS  token 获取成功")
    except Exception as exc:
        print(f"  FAIL  {exc}")
        return 1

    print("[3/3] 草稿接口权限")
    try:
        token = get_token(appid, secret)
        data = request_json(f"{API_BASE}/cgi-bin/draft/count?access_token={token}")
        check_result(data, "total_count", "查草稿数")
        print("  PASS  草稿接口可调用")
    except Exception as exc:
        print(f"  FAIL  {exc}")
        print("        草稿接口不可用就走手动复制，不影响前 3 步流程")
        ok = False

    if ok:
        print("\n三项全绿，可以用 push_draft.py 推草稿了。最后发布仍需人工点。")
        return 0
    print("\n草稿接口不通。别在这卡住，改用手动复制存草稿即可。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
