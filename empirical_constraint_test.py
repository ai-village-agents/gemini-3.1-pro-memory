import os
import json
import random
import string

def generate_dummy_content(target_bytes):
    """Generates random alphanumeric content of exactly target_bytes length."""
    return ''.join(random.choices(string.ascii_letters + string.digits + " \n", k=target_bytes))

def create_test_file(filename, byte_size):
    content = generate_dummy_content(byte_size)
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created {filename} with size {len(content)} bytes.")
    
def generate_test_suite():
    print("Generating consolidation constraint test suite...")
    sizes = [1000, 2500, 5000, 7000, 7400, 7500, 8000]
    
    os.makedirs("constraint_tests", exist_ok=True)
    
    for size in sizes:
        filename = f"constraint_tests/test_consolidation_{size}_chars.txt"
        create_test_file(filename, size)
        
    print(f"Generated {len(sizes)} test files in 'constraint_tests/' directory.")
    print("To test: copy the contents of a file and attempt consolidation.")
    
if __name__ == "__main__":
    generate_test_suite()
