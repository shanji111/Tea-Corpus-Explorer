# Tea Corpus Explorer

## 项目简介
这是一个关于茶文化的数字人文项目，包含数据处理脚本和Web前端展示。

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


## 运行Web应用
Web前端位于 `web` 目录下。

### 方法 1: 使用 PyCharm
1. 在 PyCharm 中打开此项目。
2. 配置 Python 解释器。
3. 右键点击 `run_server.py` 并选择 "Run 'run_server'"。
4. 打开浏览器访问 `http://localhost:8000/anthology.html`。

### 方法 2: 命令行
```bash
python run_server.py
```
