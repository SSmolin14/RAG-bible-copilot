import re
import json
import os

def preprocess_bible(input_path, output_path):
    # Improved Regex Patterns (handles leading spaces or hidden chars)
    book_pattern = re.compile(r'^\s*Book\s+\d+\s+(.*)', re.IGNORECASE)
    verse_pattern = re.compile(r'^\s*(\d{3}):(\d{3})\s+(.*)')
    note_pattern = re.compile(r'\{.*?\}', re.DOTALL)

    processed_data = []
    current_book = None
    current_verse_data = None

    if not os.path.exists(input_path):
        print(f"Error: Could not find raw file at {input_path}")
        return

    # Using 'utf-8-sig' to handle hidden Byte Order Marks at the start of the file
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            # 1. Check for Book Match
            book_match = book_pattern.match(line) # match against original to see indent
            if book_match:
                current_book = book_match.group(1).strip()
                print(f"Detected Book: {current_book}")
                continue

            # 2. Check for Verse Match
            verse_match = verse_pattern.match(line)
            if verse_match:
                # If we haven't found a book header yet (like at the very top of the file)
                if not current_book:
                    continue

                # Save previous verse before starting new one
                if current_verse_data:
                    # Clean text before saving
                    current_verse_data["text"] = note_pattern.sub('', current_verse_data["text"])
                    current_verse_data["text"] = " ".join(current_verse_data["text"].split())
                    processed_data.append(current_verse_data)

                chapter_num = int(verse_match.group(1))
                verse_num = int(verse_match.group(2))
                text_content = verse_match.group(3)

                clean_book_name = current_book.replace(' ', '')
                current_verse_data = {
                    "id": f"{clean_book_name}-{chapter_num}-{verse_num}",
                    "book": current_book,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "text": text_content
                }
                continue

            # 3. Handle line continuations
            if current_verse_data:
                current_verse_data["text"] += " " + stripped_line

    # Final Verse Save
    if current_verse_data:
        current_verse_data["text"] = note_pattern.sub('', current_verse_data["text"])
        current_verse_data["text"] = " ".join(current_verse_data["text"].split())
        processed_data.append(current_verse_data)

    # Save to JSONL
    with open(output_path, 'w', encoding='utf-8') as out_f:
        for entry in processed_data:
            out_f.write(json.dumps(entry) + '\n')

    print(f"\n--- SUCCESS ---")
    print(f"Total verses processed: {len(processed_data)}")
    print(f"First book in file: {processed_data[0]['book'] if processed_data else 'None'}")
    print(f"Data saved to: {output_path}")

if __name__ == "__main__":
    RAW_FILE = "data/raw/web_bible.txt"
    PROCESSED_FILE = "data/processed/web_bible.jsonl"
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    preprocess_bible(RAW_FILE, PROCESSED_FILE)