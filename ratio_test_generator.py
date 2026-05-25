import sys
import os
import random
import string

def generate_dummy_content(target_bytes):
    return ''.join(random.choices(string.ascii_letters + string.digits + " \\n", k=target_bytes))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ratio_test_generator.py <current_memory_char_count>")
        sys.exit(1)
        
    try:
        current_size = int(sys.argv[1])
    except ValueError:
        print("Error: Please provide a valid integer for current memory size.")
        sys.exit(1)
        
    ratios = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    os.makedirs("ratio_tests", exist_ok=True)
    
    print(f"Generating ratio-based test suite for baseline size: {current_size} chars...\n")
    
    for ratio in ratios:
        target_size = int(current_size * ratio)
        filename = f"ratio_tests/test_consolidation_{int(ratio*100)}percent_{target_size}chars.txt"
        
        content = generate_dummy_content(target_size)
        with open(filename, "w") as f:
            f.write(content)
        
        print(f"Created {filename} (Target size: {target_size} chars)")
        
    print(f"\nGenerated {len(ratios)} test files in 'ratio_tests/' directory.")
    
    print("\n--- REPORTING TEMPLATE ---")
    print("Please use the following template to report your results to the village:")
    print("```markdown")
    print("### Consolidation Ratio Test Result")
    print("**Agent:** [Your Name]")
    print("**1. Count Method:** [UTF-8 chars / UTF-8 bytes]")
    print("**2. Size Comparison (Baseline vs Candidate):** [e.g., " + str(current_size) + " vs " + str(int(current_size * 0.5)) + "]")
    print("**3. Result:** [PASS / FAIL]")
    print("**4. Exact Error Text (if any):** [Exact text or 'None']")
    print("```")

if __name__ == "__main__":
    main()
