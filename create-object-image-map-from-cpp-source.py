import re
import os

def parse_cpp_files(directory):
    mappings = {}
    create_pattern = re.compile(r'create_(\w+)')
    class_pattern = re.compile(r'class\s+(\w+)\s*:')
    image_pattern = re.compile(r'set_image\(get_internal_image\((\d+)\)\)')

    for filename in os.listdir(directory):
        if filename.startswith('objects') and filename.endswith('.cpp'):
            with open(os.path.join(directory, filename), 'r') as file:
                content = file.read()

                # Find all create_* functions
                creates = create_pattern.findall(content)

                for create in creates:
                    # Find the corresponding class
                    class_match = re.search(rf'class\s+(\w+{create})\s*:', content)
                    if class_match:
                        class_name = class_match.group(1)

                        # Find the image number within the class definition
                        class_content = content[class_match.start():]
                        image_match = image_pattern.search(class_content)
                        if image_match:
                            image_number = image_match.group(1)
                            mappings[f'create_{create}'] = f'fp1-img-{image_number}.png'

    return mappings

def write_mapping_file(mappings, output_file):
    with open(output_file, 'w') as file:
        for create, image in mappings.items():
            file.write(f'{create} = {image}\n')

# Usage
cpp_directory = 'path/to/your/cpp/files'
output_file = 'object_image_mappings.txt'

mappings = parse_cpp_files(cpp_directory)
write_mapping_file(mappings, output_file)

print(f"Mapping file '{output_file}' has been created with {len(mappings)} entries.")