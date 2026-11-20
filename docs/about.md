# GitHub 仓库简介（About）

> 本文件是给你复制用的，GitHub 不会自动读取。
> 填写位置：仓库主页右侧 About 栏 → 齿轮图标 → 勾选 Description / Topics → 保存。

---

## 一、Description（推荐：中文精准版）

```
给内容创作者的通用 AI 写作流水线：选题→写稿→去AI味→排版→存草稿。提示词来自实战蒸馏——标题规则、去套话清单、事实核对标记一应俱全；换主题即可迁移，纯文本不绑工具、零环境门槛。可选脚本已踩平微信草稿的字数、图片、报错坑。发布前的人工把关始终在你手里。
```

**为什么推荐这版：** 每一句都能在仓库里找到对应文件，没有一句空话。

| 简介里的说法 | 仓库里的依据 |
|---|---|
| 实战蒸馏的提示词 | `prompts/02-writing/` 三份文件，开头即注明蒸馏来源 |
| 标题规则 | `title-variants.md`：三组共 10 个备选、32 字上限、禁套路清单 |
| 去套话清单 | `de-ai-polish.md`：必删 6 条、必改 6 条、红线 4 条 |
| 事实核对标记 | `article-draft.md`：【需核对】+ 独立清单，责任在人 |
| 不绑工具、零环境门槛 | `docs/quickstart.md`：纯复制提示词，不装环境、不填密钥 |
| 踩平微信草稿的坑 | `push_draft.py` + `wx_api.py`：标题前置拦截、正文图自动换域名、错误码中文翻译 |
| 人工把关 | 流程最后一环永远是人工点发布，脚本不含群发 |

字符数：129（已实测），在 350 上限内。

---

## 二、备选版本（挑一个，别混着填）

### A. 英文国际版（国际曝光最大，309 字符）

```
A reusable AI writing pipeline for creators: topic to draft to de-AI polish to layout to WeChat draft box. Battle-tested prompts with title rules, AI-tone checklists and fact-check flags. Tool-agnostic, no setup. Optional script handles WeChat title, image and error pitfalls. You keep the final publish call.
```

### B. 中英双语版（两头兼顾，150 字符）

```
通用 AI 写作流水线：选题→写稿→去AI味→排版→存草稿，换主题即可迁移。实战蒸馏的标题规则+去套话清单+事实核对标记，纯文本零门槛。Reusable tool-agnostic AI writing workflow with battle-tested prompts. 人工把关始终在你手里。
```

### C. 中文精准版（见上面"推荐"）

---

## 三、Topics（建议填这 14 个）

GitHub 搜索和"相关推荐"主要靠 topics 匹配，比 Description 更影响曝光。按重要性排序：

**高流量入口（搜索量大）：**

```
ai-writing
prompt-engineering
content-creation
llm
automation
chatgpt
```

**垂直精准（竞争小、意图强）：**

```
wechat
wechat-official-account
ai-content
prompt-library
writing-assistant
markdown-to-html
chinese
```

填充顺序：先填前 6 个吃搜索量，再填后 8 个吃精准匹配。20 个上限不用填满，14 个足够。

---

## 四、Website

**建议留空。**

理由：账号主体是家人实名、本人公职身份，仓库保持纯工具定位，不往外挂个人账号链接。如果以后想放，用项目文档页，不要放公众号主页。

---

## 五、填写步骤

1. 打开仓库主页
2. 右侧 About 栏，点齿轮图标
3. Description 粘贴选中的版本（纯文本，不支持 Markdown，别加反引号）
4. Topics 逐个粘贴上面的标签
5. Website 留空
6. Save changes

---

## 六、信息缺口与处理原则

重写简介时发现三处信息不足，处理方式如下，避免写进任何未经证实的话：

| 缺口 | 处理 |
|---|---|
| 无使用人数、star 数、节省时间实测、用户案例 | 收益只写功能上必然成立的确定收益（如"不用从零搭结构""不用自己试错微信草稿的坑"），**不写任何数字** |
| 无正式产品名，README 标题用仓库名代替 | 暂用仓库名，待定名后统一替换简介与 README 标题 |
| 无流程截图或演示动图 | 文案补不了，属于后续可视化工作 |

README 首屏已同步重写，补上了痛点表、适用场景和实际收益，与本简介口径一致。

---

## 七、简介之外的两个星数杠杆

简介负责"被搜到、被点开"，下面两件事负责"点开后愿意 star"：

1. **README 首屏**——已同步重写，痛点、场景、收益逐项对应仓库里的真实文件，和本简介同一口径。
2. **发布渠道**——发到中文开发者社区（掘金、少数派、即刻）时，标题里带"公众号 AI 工作流""提示词开源"这类搜索词，比仓库简介本身带来的初始曝光大得多。
