import os
import argparse

def search_repo(query, repo_path="."):
    print(f"Searching exo-memory for: '{query}'\n")
    results = []
    for root, dirs, files in os.walk(repo_path):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append((file_path, content))
                        
    if not results:
        print("No matches found.")
    else:
        for path, content in results:
            print(f"--- Found in {path} ---")
            # Print a snippet around the match
            idx = content.lower().find(query.lower())
            start = max(0, idx - 100)
            end = min(len(content), idx + 200)
            print(f"...{content[start:end]}...\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Gemini 3.1 Pro Exo-Memory")
    parser.add_argument("query", type=str, help="The search term")
    args = parser.parse_args()
    search_repo(args.query)
