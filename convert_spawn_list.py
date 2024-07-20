import re
import sys


def convert_spawn_list(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file:
        content = input_file.read()

    # print(content)
    # Extract relevant spawn commands
    print(f"Searching for level info in {input_file}")
    spawn_commands = re.findall(r'add_(?:background_)?object\((.*?)\);', content)

    # Extract object names and remove duplicates
    object_names = set()
    for command in spawn_commands:
        match = re.match(r'create_(\w+)', command)
        if match:
            object_names.add(match.group(1))

    rgx_index = r'index = (\d+);'
    rgx_width = r'width = (\d+);'
    rgx_height = r'height = (\d+);'
    rgx_virtual_width = r'virtual_width = (\d+);'
    rgx_virtual_height = r'virtual_height = (\d+);'
    #rgx_background_color = r'background_color = (\N+);'

    val_index = re.search(rgx_index, content)
    val_width = re.search(rgx_width, content)
    val_height = re.search(rgx_height, content)
    val_virtual_width = re.search(rgx_virtual_width, content)
    val_virtual_height = re.search(rgx_virtual_height, content)
    #val_background_color = re.search(rgx_background_color, content)

    # Check if all values were found
    if not all([val_index, val_width, val_height, val_virtual_width, val_virtual_height]):
        print("Error: Not all required values were found in the input file.")
        return

    # Extract values
    val_index = val_index.group(1)
    val_width = val_width.group(1)
    val_height = val_height.group(1)
    val_virtual_width = val_virtual_width.group(1)
    val_virtual_height = val_virtual_height.group(1)
    #val_background_color = val_background_color.group(1)

    mapping_filename = f"frame_{int(val_index) + 1}_mappings.txt"
    # Example line from mapping file: create_mapdata_27 = fp1-img-3656.png
    # Gotta do a split and trim nd we should bre able to auto-map the command to the image.

    with open(output_file_path, 'w') as output_file:
        print(f"Writing new Unity MonoBehavior Spawnlist to: {output_file_path}")

        # Write Sprite and Collider declarations
        output_file.write("public class SpawnDV1 : FP1LevelSpawn\n{\n")
        output_file.write("    public bool enableScaleUpForFP2SizedCharacters = true;\n\n")
        output_file.write(f"    public string mapping_filename = \"{mapping_filename}\";\n\n")
        for obj_name in object_names:
            output_file.write(f"    public Sprite {obj_name};\n")
        output_file.write("\n")
        for obj_name in object_names:
            output_file.write(f"    public GameObject {obj_name}_collider;\n")
        output_file.write("\n")

        output_file.write("void Start()\n{\n")
        output_file.write(f"    var index = {val_index};\n")
        output_file.write(f"    var width = {val_width};\n")
        output_file.write(f"    var height = {val_height};\n")
        output_file.write(f"    var virtual_width = {val_virtual_width};\n")
        output_file.write(f"    var virtual_height = {val_virtual_height};\n")
        # output_file.write(f"    var background_color = new {val_background_color};\n")
        # output_file.write(f"    int timer_base = 0;\n\n")

        output_file.write("    if (spawnedLevelContainer == null)\n")
        output_file.write("    {\n")
        output_file.write("        spawnedLevelContainer = new GameObject(\"spawnedLevelContainer\");\n")
        output_file.write("    }\n\n")

        for command in spawn_commands:
            output_file.write(f"    add_background_object({command});\n")

        output_file.write("\n    // This needs to happen last in order to scale all of the included objects with it.\n")
        output_file.write("    if (enableScaleUpForFP2SizedCharacters && spawnedLevelContainer != null)\n")
        output_file.write("    {\n")
        output_file.write("        spawnedLevelContainer.transform.localScale = new Vector3(fp2ScaleFactor, fp2ScaleFactor, 0);\n")
        output_file.write("    }\n")
        output_file.write("}\n")

# Usage convert_spawn_list('path/to/input/spawn_list.txt', 'path/to/output/fp2_spawn_list.cs')

if __name__ == "__main__":
    print('Usage: python3 convert_spawn_list.py <input_file_path> <output_file_path>')
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    convert_spawn_list(input_file, output_dir)
