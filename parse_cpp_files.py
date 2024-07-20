import re
import os
import sys


def parse_cpp_files(directory, create_tokens):
    mappings = {}
    class_pattern = re.compile(r'class\s+(\w+)\s*:')
    image_pattern = re.compile(r'get_internal_image\((\d+)\)')

    for filename in os.listdir(directory):
        if filename.startswith('objects') and filename.endswith('.cpp'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

                for token in create_tokens:
                    class_name = token.replace('create_', '')
                    class_match = re.search(rf'class\s+(\w*{re.escape(class_name)})\s*:', content, re.IGNORECASE)
                    if class_match:
                        full_class_name = class_match.group(1)

                        class_content = content[class_match.start():]
                        image_match = image_pattern.search(class_content)
                        if image_match:
                            image_number = image_match.group(1)
                            mappings[token] = f'fp1-img-{image_number}.png'
                        else:
                            print(f"Warning: No image found for {token} in {filename}")
                    # else:
                        # print(f"Warning: No class found for {token} in {filename}")
                        # We commented it out because it's very slow, but useful for debugging.
    return mappings


def write_mapping_file(mappings, output_file):
    with open(output_file, 'w') as file:
        for create, image in mappings.items():
            file.write(f'{create} = {image}\n')


if len(sys.argv) < 3:
    print(
        "Usage: python script.py <cpp_directory> <output_file> --file <tokens_file> OR <create_token1> <create_token2> ...")
    sys.exit(1)

cpp_directory = sys.argv[1]
output_file = sys.argv[2]

create_tokens = []
if "--file" in sys.argv:
    tokens_file_index = sys.argv.index("--file") + 1  # the argument after --file
    with open(sys.argv[tokens_file_index], 'r') as f:
        create_tokens = [line.strip() for line in f]
else:
    create_tokens = sys.argv[3:]

mappings = parse_cpp_files(cpp_directory, create_tokens)
write_mapping_file(mappings, output_file)

print(f"Mapping file '{output_file}' has been created with {len(mappings)} entries.")
for token in create_tokens:
    if token not in mappings:
        print(f"Warning: No mapping found for {token}")
