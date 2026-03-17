import http.server
import socketserver
import json
import glob
import os
import urllib.parse
import re

PORT = 8000
DIRECTORY = "web"
DATA_DIR = os.path.join(DIRECTORY, "data", "my_json")

# In-memory corpus storage
corpus_data = []

def load_corpus():
    print("Loading corpus from JSON files...")
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Normalize keys and add metadata
                normalized_data = {}
                
                # Extract ID and Decade from filename (e.g., 1820_1.json)
                filename = os.path.basename(file_path)
                match = re.match(r"(\d+)_(\d+)\.json", filename)
                
                file_decade = 0
                file_id = 0
                if match:
                    file_decade = int(match.group(1))
                    file_id = int(match.group(2))
                
                # Handle potential case variations or missing keys
                year = data.get('Year') or data.get('year')
                genre = data.get('Genre') or data.get('genre')
                text = data.get('Text') or data.get('text')
                
                if year is not None:
                    try:
                        normalized_data['year'] = int(year)
                        normalized_data['decade'] = (normalized_data['year'] // 10) * 10
                    except ValueError:
                        normalized_data['year'] = 0
                        normalized_data['decade'] = file_decade
                else:
                    normalized_data['year'] = 0
                    normalized_data['decade'] = file_decade
                    
                normalized_data['genre'] = str(genre) if genre else "Unknown"
                normalized_data['text'] = str(text) if text else ""
                normalized_data['source_file'] = filename
                normalized_data['id'] = file_id
                
                corpus_data.append(normalized_data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    print(f"Loaded {len(corpus_data)} documents.")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/api/search':
            self.handle_search(parsed_path.query)
        elif parsed_path.path == '/api/document':
            self.handle_document(parsed_path.query)
        else:
            super().do_GET()

    def handle_document(self, query_string):
        params = urllib.parse.parse_qs(query_string)
        doc_id = params.get('id', [''])[0].strip()
        decade = params.get('decade', [''])[0].strip()
        
        if not doc_id:
            self.send_error(400, "Missing id parameter")
            return

        try:
            target_id = int(doc_id)
            target_decade = int(decade) if decade else None
            
            found = None
            for doc in corpus_data:
                if doc['id'] == target_id:
                    if target_decade is not None:
                        if doc['decade'] == target_decade:
                            found = doc
                            break
                    else:
                        found = doc
                        break
            
            if found:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(found).encode('utf-8'))
            else:
                self.send_error(404, "Document not found")
                
        except ValueError:
            self.send_error(400, "Invalid id format")

    def handle_search(self, query_string):
        params = urllib.parse.parse_qs(query_string)
        
        query_text = params.get('q', [''])[0].strip()
        decade_filter = params.get('decade', [''])[0].strip()
        genre_filter = params.get('genre', [''])[0].strip()
        sort_order = params.get('sort', ['asc'])[0].strip()
        
        results = corpus_data
        
        # Filter by text query
        if query_text:
            try:
                pattern = re.compile(rf"\b{re.escape(query_text)}\b", re.IGNORECASE)
                results = [doc for doc in results if pattern.search(doc['text'])]
            except re.error:
                query_lower = query_text.lower()
                results = [doc for doc in results if query_lower in doc['text'].lower()]
        else:
            results = []

        # Filter by decade
        if decade_filter:
            try:
                decade_val = int(decade_filter)
                results = [doc for doc in results if doc['decade'] == decade_val]
            except ValueError:
                pass

        # Filter by genre
        if genre_filter:
             results = [doc for doc in results if doc['genre'] == genre_filter]

        # Sort
        reverse = (sort_order == 'desc')
        results.sort(key=lambda x: x['year'], reverse=reverse)
        
        # Limit results
        results = results[:200]
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode('utf-8'))

if __name__ == '__main__':
    load_corpus()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
