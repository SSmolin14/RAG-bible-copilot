import json
import os

def create_chunks(input_path, output_path, window_size=3, overlap=1):
    """
    Groups individual verses into overlapping chunks to provide 
    better context for the LLM.
    """
    chunks = []
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    # 1. Load the structured verses
    with open(input_path, 'r', encoding='utf-8') as f:
        verses = [json.loads(line) for line in f]

    # 2. Group by Book (important: don't bridge Revelation into Genesis!)
    books = {}
    for v in verses:
        books.setdefault(v['book'], []).append(v)

    # 3. Create sliding windows within each book
    for book_name, book_verses in books.items():
        i = 0
        while i < len(book_verses):
            # Take a slice of verses (e.g., verses 1, 2, 3)
            chunk_slice = book_verses[i : i + window_size]
            
            # If we are at the very end of a book and have a tiny leftover, 
            # the slice might be smaller than window_size, which is fine.
            combined_text = " ".join([v['text'] for v in chunk_slice])
            
            # Create a clean citation string
            start_v = chunk_slice[0]
            end_v = chunk_slice[-1]
            
            if start_v['verse'] == end_v['verse']:
                citation = f"{book_name} {start_v['chapter']}:{start_v['verse']}"
            else:
                citation = f"{book_name} {start_v['chapter']}:{start_v['verse']}-{end_v['verse']}"
            
            chunks.append({
                "chunk_id": f"{start_v['id']}_w{window_size}_o{overlap}",
                "text": combined_text,
                "metadata": {
                    "citation": citation,
                    "book": book_name,
                    "chapter": start_v['chapter'],
                    "start_verse": start_v['verse'],
                    "end_verse": end_v['verse']
                }
            })
            
            # Move the window forward
            # If window_size=3 and overlap=1, we move forward by 2 (3-1=2)
            i += (window_size - overlap)
            
            # Prevent infinite loops
            if window_size <= overlap:
                break

    # 4. Save the chunks
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for chunk in chunks:
            out_f.write(json.dumps(chunk) + '\n')

    print(f"Successfully created {len(chunks)} chunks from {len(verses)} verses.")

if __name__ == "__main__":
    PROCESSED_FILE = "data/processed/web_bible.jsonl"
    CHUNK_FILE = "data/processed/web_chunks.jsonl"
    
    create_chunks(PROCESSED_FILE, CHUNK_FILE)