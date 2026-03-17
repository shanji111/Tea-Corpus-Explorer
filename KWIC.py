from pathlib import Path
import pandas as pd
import re

# ===== 1. 文件路径 =====
data_dir = Path(r"E:\COHA\tea_bydecade")
input_file = data_dir / "all_corpus_texts.xlsx"
output_file = data_dir / "tea_hits.xlsx"

# ===== 2. 读取总表 =====
df = pd.read_excel(input_file)

# ===== 3. 基本清理 =====
df.columns = df.columns.str.strip().str.lower()

required_cols = {"id", "year", "decade", "genre", "text", "source_file", "row_in_file"}
missing_cols = required_cols - set(df.columns)

if missing_cols:
    raise ValueError(f"总表缺少这些列: {missing_cols}")

df = df.dropna(subset=["text"])
df["text"] = df["text"].astype(str)

# ===== 4. 设定关键词 =====
keyword = "tea"

# 只匹配完整单词 tea，不匹配 teapot / tea-table 这种更长形式
pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)

# ===== 5. 提取命中 =====
results = []
hit_id = 1

for _, row in df.iterrows():
    text = row["text"]

    for match in pattern.finditer(text):
        start, end = match.span()

        # 左右语境窗口长度：按字符数截取
        window = 40

        left_context = text[max(0, start - window):start].strip()
        hit_word = text[start:end]
        right_context = text[end:min(len(text), end + window)].strip()

        results.append({
            "id": hit_id,
            "corpus_text_id": row["id"],
            "keyword": keyword,
            "keyword_normalized": keyword.lower(),
            "left_context": left_context,
            "hit_word": hit_word,
            "right_context": right_context,
            "year": row["year"],
            "decade": row["decade"],
            "genre": row["genre"],
            "source_file": row["source_file"],
            "row_in_file": row["row_in_file"],
            "match_start": start,
            "match_end": end,
            "is_valid": True,
            "notes": ""
        })

        hit_id += 1

# ===== 6. 转成 DataFrame =====
hits_df = pd.DataFrame(results)

# ===== 7. 保存输出 =====
hits_df.to_excel(output_file, index=False)

print("提取完成！")
print(f"共找到 {len(hits_df)} 条 tea 命中")
print(f"输出文件: {output_file}")

if len(hits_df) > 0:
    print("\\n前 5 条预览：")
    print(hits_df.head())
else:
    print("\\n没有找到 tea，请检查文本内容或关键词设定。")