from pathlib import Path
import pandas as pd
import re

# 1. 你的文件夹路径
data_dir = Path(r"E:\COHA\tea_bydecade")

# 2. 只匹配主文件：tea_1820.xlsx、tea_1830.xlsx ...
pattern = re.compile(r"^tea_(\d{4})\.xlsx$", re.IGNORECASE)

# 3. 找到所有符合条件的 xlsx 文件
excel_files = []
for file_path in data_dir.glob("*.xlsx"):
    if pattern.match(file_path.name):
        excel_files.append(file_path)

excel_files = sorted(excel_files)

print("找到的主文件有：")
for f in excel_files:
    print(" -", f.name)

all_dfs = []
global_id = 1

for file_path in excel_files:
    print(f"\n正在处理: {file_path.name}")

    # 读取 Excel
    df = pd.read_excel(file_path)

    # 清理列名
    df.columns = df.columns.str.strip().str.lower()

    # 检查必要列
    required_cols = {"year", "genre", "text"}
    missing_cols = required_cols - set(df.columns)

    if missing_cols:
        print(f"跳过 {file_path.name}，缺少列: {missing_cols}")
        continue

    # 删除 text 为空的行
    df = df.dropna(subset=["text"])
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"] != ""]

    # year 转为整数
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    # genre 标准化
    df["genre"] = df["genre"].astype(str).str.strip().str.upper()

    # 增加辅助列
    df["row_in_file"] = range(1, len(df) + 1)
    df["source_file"] = file_path.name
    df["decade"] = (df["year"] // 10) * 10
    df["id"] = range(global_id, global_id + len(df))
    global_id += len(df)

    # 调整列顺序
    df = df[["id", "year", "decade", "genre", "text", "source_file", "row_in_file"]]

    all_dfs.append(df)

# 4. 合并并输出
if all_dfs:
    merged_df = pd.concat(all_dfs, ignore_index=True)
    merged_df = merged_df.sort_values(by=["year", "id"]).reset_index(drop=True)

    output_path = data_dir / "all_corpus_texts.xlsx"
    merged_df.to_excel(output_path, index=False)

    print(f"\n合并完成！")
    print(f"总记录数: {len(merged_df)}")
    print(f"输出文件: {output_path}")
    print("\n前 5 行预览：")
    print(merged_df.head())
else:
    print("没有找到可合并的主文件，请检查文件名或路径。")