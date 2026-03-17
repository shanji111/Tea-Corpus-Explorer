from pathlib import Path
import pandas as pd
import re

# ===== 1. 文件路径 =====
data_dir = Path(r"E:\COHA\tea_bydecade")
input_file = data_dir / "tea_hits.xlsx"
output_file = data_dir / "tea_hits_cleaned.xlsx"

# ===== 2. 读取文件 =====
df = pd.read_excel(input_file)
df.columns = df.columns.str.strip().str.lower()

print(f"原始命中数: {len(df)}")

# ===== 3. 检查必要列 =====
required_cols = {
    "id", "corpus_text_id", "keyword", "left_context", "hit_word", "right_context",
    "year", "decade", "genre", "source_file"
}
missing_cols = required_cols - set(df.columns)

if missing_cols:
    raise ValueError(f"tea_hits.xlsx 缺少这些列: {missing_cols}")

# ===== 4. 基本清理 =====
# 去掉关键列为空的行
df = df.dropna(subset=["left_context", "hit_word", "right_context"])

# 全部转成字符串，去掉首尾空格
for col in ["left_context", "hit_word", "right_context", "keyword", "genre", "source_file"]:
    df[col] = df[col].astype(str).str.strip()

# ===== 5. 只保留真正的 tea 命中 =====
df = df[df["hit_word"].str.lower() == "tea"]

# ===== 6. 去重 =====
# 如果左右语境+年份+体裁都一样，基本可视为重复
df = df.drop_duplicates(
    subset=["left_context", "hit_word", "right_context", "year", "genre"]
).copy()

# ===== 7. 定义一些过滤函数 =====
def count_letters(text):
    return len(re.findall(r"[A-Za-z]", text))

def count_words(text):
    return len(re.findall(r"\b[A-Za-z]+\b", text))

def symbol_ratio(text):
    if not text:
        return 1.0
    symbols = re.findall(r"[^A-Za-z0-9\s.,;:!?'\-]", text)
    return len(symbols) / max(len(text), 1)

def looks_too_noisy(left, right):
    full = f"{left} {right}".strip()

    # 字母太少：大概率是残片或乱码
    if count_letters(full) < 8:
        return True

    # 单词太少：上下文太碎
    if count_words(full) < 2:
        return True

    # 奇怪符号比例太高
    if symbol_ratio(full) > 0.15:
        return True

    return False

def context_too_short(left, right):
    # 左右总长度过短，通常不利于展示
    return (len(left.strip()) + len(right.strip())) < 12

# ===== 8. 应用过滤 =====
mask_not_short = ~df.apply(lambda row: context_too_short(row["left_context"], row["right_context"]), axis=1)
df = df[mask_not_short].copy()

mask_not_noisy = ~df.apply(lambda row: looks_too_noisy(row["left_context"], row["right_context"]), axis=1)
df = df[mask_not_noisy].copy()

# ===== 9. 增加清洗标记 =====
df["clean_status"] = "auto_kept"

# ===== 10. 重新编号（可选） =====
df = df.reset_index(drop=True)
df["clean_id"] = range(1, len(df) + 1)

# 把 clean_id 放前面
cols = ["clean_id"] + [c for c in df.columns if c != "clean_id"]
df = df[cols]

# ===== 11. 保存 =====
df.to_excel(output_file, index=False)

print(f"清洗后命中数: {len(df)}")
print(f"输出文件: {output_file}")

print("\n前 5 条预览：")
print(df.head())