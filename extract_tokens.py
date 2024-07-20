import os
import re
import sys

def extract_unique_tokens(input_file, output_folder):
    token_pattern = re.compile(r'create_(\w+)')
    unique_tokens = set()

    with open(input_file, 'r') as f:
        for line in f:
            matches = token_pattern.findall(line)
            unique_tokens.update(f"create_{token}" for token in matches)

    # Get the base name from the input file
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # Construct the new filename based on the base name
    new_filename = base_name + '_tokens.txt'
    # Create the full path for the new output file
    output_file = os.path.join(output_folder, new_filename)

    with open(output_file, 'w') as f:
        for token in sorted(unique_tokens):
            f.write(f"{token}\n")

    print(f"Found {len(unique_tokens)} unique create tokens.")
    print(f"Unique tokens have been written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_tokens.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]
    extract_unique_tokens(input_file, output_folder)