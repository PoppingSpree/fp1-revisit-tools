import re
import os
import sys

def extract_frame_init(input_file, output_dir):
    frame_pattern = re.compile(r'void Frames::on_frame_(\d+)_init\(\)\s*{')
    end_pattern = re.compile(r'^\}')

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    matches = frame_pattern.finditer(content)
    for match in matches:
        frame_number = match.group(1)
        start_pos = match.start()

        # Find the end of the function
        brace_count = 1
        end_pos = start_pos
        for line in content[start_pos:].split('\n')[1:]:
            end_pos += len(line) + 1  # +1 for the newline
            if '{' in line:
                brace_count += line.count('{')
            if '}' in line:
                brace_count -= line.count('}')
            if brace_count == 0:
                break

        function_content = content[start_pos:end_pos]

        # Write to output file
        output_file = os.path.join(output_dir, f"frame_{frame_number}_init.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(function_content)

        print(f"Extracted frame {frame_number} init to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_frame_init.py <input_file> <output_directory>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    extract_frame_init(input_file, output_dir)