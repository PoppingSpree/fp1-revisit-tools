import re
import os
import sys

def parse_cpp_files(directory, create_tokens):
    mappings = {}
    class_pattern = re.compile(r'class\s+(\w+)\s*:')
    image_pattern = re.compile(r'set_image\(get_internal_image\((\d+)\)\)')

    for filename in os.listdir(directory):
        if filename.startswith('objects') and filename.endswith('.cpp'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

                for token in create_tokens:
                    # Find the corresponding class
                    class_name = token.replace('create_', '')
                    class_match = re.search(rf'class\s+(\w*{re.escape(class_name)})\s*:', content)
                    if class_match:
                        full_class_name = class_match.group(1)

                        # Find the image number within the class definition
                        class_content = content[class_match.start():]
                        image_match = image_pattern.search(class_content)
                        if image_match:
                            image_number = image_match.group(1)
                            mappings[token] = f'fp1-img-{image_number}.png'
                        else:
                            print(f"Warning: No image found for {token} in {filename}")
                    else:
                        print(f"Warning: No class found for {token} in {filename}")

    return mappings

def write_mapping_file(mappings, output_file):
    with open(output_file, 'w') as file:
        for create, image in mappings.items():
            file.write(f'{create} = {image}\n')

# Usage
if len(sys.argv) < 3:
    print("Usage: python script.py <cpp_directory> <output_file> <create_token1> <create_token2> ...")
    sys.exit(1)

cpp_directory = sys.argv[1]
output_file = sys.argv[2]
create_tokens = sys.argv[3:]

mappings = parse_cpp_files(cpp_directory, create_tokens)
write_mapping_file(mappings, output_file)

print(f"Mapping file '{output_file}' has been created with {len(mappings)} entries.")
for token in create_tokens:
    if token not in mappings:
        print(f"Warning: No mapping found for {token}")