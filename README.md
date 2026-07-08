# Tea Corpus Explorer

> A corpus-based digital humanities platform for exploring the historical representation of “tea” in English and American literary texts.

## 项目简介
Tea Corpus Explorer 是“TEA（茶）在英美文学作品中的形象流变——计量文体学视角”项目的成果展示与语料检索平台。本项目以 17 世纪中叶至当代英美文学文本为语料背景，围绕 “tea（茶）” 这一具有中华文化属性和跨文化传播意义的文化意象，考察其在英美文学中的语义演变、文化功能重构与读者接受。

本平台旨在将项目中的语料、文本样例、关键词共现、搭配关系和可视化结果集中展示，使研究过程和主要发现能够以更直观、可检索、可复核的方式呈现。

在线访问地址：http://tea-corpus-explorer-master.rixinfy.com/

## 研究背景

茶不仅是一种日常饮品，也是一种具有跨文化意义的文学和文化符号。自茶进入英语世界以来，`tea` 在英美文学中逐渐经历了从东方舶来奢侈品，到社交礼仪与日常生活符号，再到民族文化与身份象征的历时转变。

既有研究多依赖个案文本细读，较少系统追踪 `tea` 在长时段英美文学文本中的共现模式、句法功能、语义邻域和情感色彩变化。本项目尝试结合语料库语言学、计量文体学、自然语言处理和读者问卷验证，为文化意象研究提供更可复核的证据链。

## 核心功能

- `tea` 相关文本检索
- 文学文本样例展示
- 关键词共现分析
- 搭配关系观察
- 相关文本上下文查看
- 项目研究结果可视化展示

平台支持用户围绕 `tea` 及相关关键词进行检索，观察其在不同文本语境中的搭配对象和文化意义变化。用户也可以通过文本展示进一步查看具体语境，从而理解 `tea` 如何在英美文学中被不断重构为文化符号。

## 依赖安装
请确保安装了以下Python库：
```bash
pip install -r requirements.txt
```

## 数据处理
项目包含多个Python脚本用于处理原始语料数据：
- `KWIC.py`: 从总表提取关键词上下文 (生成 `tea_hits.xlsx`)
- `clean.py`: 清洗提取的命中数据 (生成 `tea_hits_cleaned.xlsx`)
- `make_display_text.py`: 生成用于展示的文本数据 (生成 `all_corpus_texts_display.xlsx` 和 `all_corpus_texts.json`)
- `to_json.py`: 将Excel数据转换为Web可用的JSON格式



## 技术方法

项目中使用或涉及的方法包括：

- Python 文本处理
- 语料清洗与结构化整理
- 关键词共现分析
- 搭配词统计
- 句法角色分析
- BERT 语义嵌入
- 情感分析
- 数据可视化
- Web 展示平台开发

## 主要发现

研究发现，`tea` 在英美文学中的文学表征并非静止不变，而是在长期跨文化传播与本土化过程中呈现出较为清晰的阶段性重构路径：

```text
异域商品 → 社交仪式 → 文化/身份符号
```
