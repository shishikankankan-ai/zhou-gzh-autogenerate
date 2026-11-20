# 文章 HTML 示例

`push_draft.py` 需要的 HTML 长这样。这是排版好的正文,可以直接拿去测试。

## 关键点

- 样式必须内联(`style="..."`),公众号会过滤 class 和外部样式表。
- 正文里放图片,用**相对路径**(相对仓库根目录),脚本会自动上传换成微信域名。比如 `examples/demo-cover.jpg`。
- 不要用外链图片(比如 `https://xxx.com/a.png`),微信会过滤掉,脚本会提醒你。
- 标题在命令行用 `--title` 传,不写在这里。

## 示例 HTML

```html
<div style="font-size:16px;line-height:1.75;color:#333;">
  <p style="margin:0 0 1em;">这是开头第一段，直接切入主题。</p>
  <h2 style="font-size:18px;font-weight:bold;margin:1.5em 0 0.5em;">第一部分</h2>
  <p style="margin:0 0 1em;">这里是正文内容。</p>
  <img src="examples/demo-cover.jpg" style="max-width:100%;" />
  <p style="margin:0 0 1em;">图片上面这行：src 用相对路径，脚本会自动上传。</p>
  <h2 style="font-size:18px;font-weight:bold;margin:1.5em 0 0.5em;">第二部分</h2>
  <p style="margin:0 0 1em;">这里是更多内容。</p>
</div>
```

## 跑一次

```bash
# 1. 复制配置、填密钥
cp .env.example .env
# 编辑 .env，填 WECHAT_APPID 和 WECHAT_SECRET

# 2. 自检
python scripts/check_env.py

# 3. 推草稿（把上面的示例 HTML 存成 output/article.html，封面放 output/cover.jpg）
python scripts/push_draft.py \
  --html output/article.html \
  --cover output/cover.jpg \
  --title "示例标题" \
  --author "作者名"
```
