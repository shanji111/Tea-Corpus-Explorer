from pathlib import Path
import pandas as pd
import re
import json

data_dir = Path(r"E:\COHA\tea_bydecade")

input_file = data_dir / "all_corpus_texts.xlsx"
output_excel = data_dir / "all_corpus_texts_display.xlsx"
output_json = data_dir / "all_corpus_texts.json"

print("正在读取文件：", input_file)

df = pd.read_excel(input_file)
df.columns = df.columns.str.strip().str.lower()

print("读取后行数：", len(df))
print("列名：", list(df.columns))
print("前3行预览：")
print(df.head(3))

def clean_display_text(text):
    t = str(text) if pd.notna(text) else ""

    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"\s+\)", ")", t)
    t = re.sub(r"\bp\.\s*[ivxlcdm0-9]+\.", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s+[—–-]{2,}\s+", " ", t)
    t = re.sub(r"([,.!?;:])([A-Za-z])", r"\1 \2", t)
    t = re.sub(r"\s{2,}", " ", t).strip()

    return t

if "text" not in df.columns:
    raise ValueError("找不到 text 列，请检查 all_corpus_texts.xlsx")

df["display_text"] = df["text"].apply(clean_display_text)

print("处理后行数：", len(df))

df.to_excel(output_excel, index=False)

records = df.fillna("").to_dict(orient="records")
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"已生成 Excel: {output_excel}")
print(f"已生成 JSON: {output_json}")
print(f"最终共 {len(df)} 条")