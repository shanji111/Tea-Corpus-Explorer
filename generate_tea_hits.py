import json
import glob
import os
import re

DATA_DIR = "web/data/my_json"
OUTPUT_FILE = "web/data/tea_hits_cleaned.json"

def generate_tea_hits():
    print("Generating tea hits from corpus...")
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    
    hits = []
    hit_id = 1
    
    # Regex for 'tea' as a whole word, case insensitive
    pattern = re.compile(r"\btea\b", re.IGNORECASE)
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            text = data.get('Text') or data.get('text') or ""
            year = data.get('Year') or data.get('year')
            genre = data.get('Genre') or data.get('genre') or "Unknown"
            
            # Extract decade/id from filename if year is missing
            filename = os.path.basename(file_path)
            match = re.match(r"(\d+)_(\d+)\.json", filename)
            file_decade = 0
            file_id = 0
            if match:
                file_decade = int(match.group(1))
                file_id = int(match.group(2))
                
            try:
                year_int = int(year)
                decade = (year_int // 10) * 10
            except (ValueError, TypeError):
                year_int = 0
                decade = file_decade

            # Find hits
            for match in pattern.finditer(text):
                start, end = match.span()
                
                # Context window 40 chars
                window = 40
                left_context = text[max(0, start - window):start].strip()
                hit_word = text[start:end]
                right_context = text[end:min(len(text), end + window)].strip()
                
                hit = {
                    "clean_id": hit_id,
                    "id": hit_id,
                    "corpus_text_id": file_id, # using file_id as corpus_text_id
                    "keyword": "tea",
                    "keyword_normalized": "tea",
                    "left_context": left_context,
                    "hit_word": hit_word,
                    "right_context": right_context,
                    "year": year_int,
                    "decade": decade,
                    "genre": genre,
                    "source_file": filename,
                    "row_in_file": 0,
                    "match_start": start,
                    "match_end": end,
                    "is_valid": True,
                    "notes": "",
                    "clean_status": "auto_kept"
                }
                hits.append(hit)
                hit_id += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Write to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(hits, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(hits)} hits. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_tea_hits()
