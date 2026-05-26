import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python count_size_simple.py <file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Character count: {len(content)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
