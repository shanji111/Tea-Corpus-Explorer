from pathlib import Path
import pandas as pd
import json

data_dir = Path(r"E:\COHA\tea_bydecade")

files = [
    ("tea_hits_cleaned.xlsx", "tea_hits_cleaned.json"),
    ("all_corpus_texts.xlsx", "all_corpus_texts.json"),
]

for excel_name, json_name in files:
    input_file = data_dir / excel_name
    output_file = data_dir / json_name

    df = pd.read_excel(input_file)
    df.columns = df.columns.str.strip().str.lower()
    df = df.fillna("")

    records = df.to_dict(orient="records")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"已生成: {output_file}，共 {len(records)} 条")