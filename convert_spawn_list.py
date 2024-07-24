import re
import sys


def convert_spawn_list(input_file_path, mapping_file_path, output_file_path):
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

    # Read mapping file
    mapping = {}
    mapping_no_create = {}
    with open(mapping_file_path, 'r') as mapping_file:
        for line in mapping_file:
            parts = line.strip().split(' = ')
            if len(parts) == 2:
                mapping[parts[0]] = parts[1]
                mapping_no_create[parts[0].replace("create_", "")] = parts[1]

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
        src_includes = """using System.Collections;
using System.Collections.Generic;
using UnityEngine;

"""
        output_file.write(src_includes)

        # Write Sprite and Collider declarations
        output_file.write(f"public class FP1Frame{int(val_index) + 1} : FP1LevelSpawn\n{{\n")
        output_file.write("    public bool enableScaleUpForFP2SizedCharacters = true;\n\n")
        output_file.write(f"    public bool hasPerformedImageLoad = false;\n\n")
        output_file.write(f"    public string mapping_filename = \"{mapping_filename}\";\n\n")

        output_file.write(f"    public int index = {val_index};\n")
        output_file.write(f"    public int width = {val_width};\n")
        output_file.write(f"    public int height = {val_height};\n")
        output_file.write(f"    public int virtual_width = {val_virtual_width};\n")
        output_file.write(f"    public int virtual_height = {val_virtual_height};\n\n")
        # output_file.write(f"    var background_color = new {val_background_color};\n")
        # output_file.write(f"    int timer_base = 0;\n\n")
        
        # for obj_name in object_names:
        #     output_file.write(f"    public Sprite {obj_name};\n")
        # output_file.write("\n")
        # for obj_name in object_names:
        #     output_file.write(f"    public GameObject {obj_name}_collider;\n")
        # output_file.write("\n")

        for obj_name, sprite_file in mapping_no_create.items():
            output_file.write(f"    public Sprite {obj_name};\n")
        output_file.write("\n")
        for obj_name, sprite_file in mapping_no_create.items():
            output_file.write(f"    public GameObject {obj_name}_collider;\n")
        output_file.write("\n")

        # Write dictionary for sprite mapping
        output_file.write("    // Dictionary to store sprite mappings\n")
        output_file.write("    private Dictionary<string, Sprite> spriteMap = new Dictionary<string, Sprite>();\n\n")


        output_file.write("    void Start()\n    {\n")

        output_file.write("        if (!hasPerformedImageLoad){\n")
        output_file.write("            hasPerformedImageLoad = true;\n")
        output_file.write("            LoadSprites();\n")
        output_file.write("        }\n")

        output_file.write("        if (spawnedLevelContainer == null)\n")
        output_file.write("        {\n")
        output_file.write("            spawnedLevelContainer = new GameObject(\"spawnedLevelContainer\");\n")
        output_file.write("        }\n\n")

        for command in spawn_commands:
            output_file.write(f"        add_background_object({command});\n")
            
        # Setting the Camera Bounds for Fall KO.
        src_set_camera_bounds = """var stageCam = GameObject.Find("Stage Camera");
        if (stageCam != null)
        {
            var fpCam = stageCam.GetComponent<FPCamera>();
            fpCam.parallaxLayers[0].xSize = width;
            fpCam.parallaxLayers[0].ySize = height;
            if (enableScaleUpForFP2SizedCharacters && spawnedLevelContainer != null)
            {
                fpCam.parallaxLayers[0].xSize *= fp2ScaleFactor;
                fpCam.parallaxLayers[0].ySize *= fp2ScaleFactor;
            }
        }
        
        """

        output_file.write(src_set_camera_bounds)

        output_file.write("\n        // This needs to happen last in order to scale all of the included objects with it.\n")
        output_file.write("        if (enableScaleUpForFP2SizedCharacters && spawnedLevelContainer != null)\n")
        output_file.write("        {\n")
        output_file.write("            spawnedLevelContainer.transform.localScale = new Vector3(fp2ScaleFactor, fp2ScaleFactor, 0);\n")
        output_file.write("        }\n")

        output_file.write("    }\n\n")

        # Write LoadSprites method
        output_file.write("    private void LoadSprites()\n    {\n")
        output_file.write("        string spritePath = \"Sprites/FP1/\";\n")

        output_file.write(f"        // Remember: For this to work you would have to put the assets in a Resources folder\n")
        output_file.write(f"        // And treat that Resources folder as if it's the root (you can have many Resource folders).\n")
        output_file.write(f"        // So in this case: Assets/YourName/Resources/Sprites/FP1/\n")
        for obj_name, sprite_file in mapping_no_create.items():
            output_file.write(f"        {obj_name} = Resources.Load<Sprite>(spritePath + \"{sprite_file.replace('.png', '')}\");\n")
        output_file.write("    }\n\n")

        sample_object_create_method_text= """
    public BGObjectInfo create_dvrockslope9_912(int xpos, int ypos)
	{
		BGObjectInfo obj = new BGObjectInfo();
		obj.name = "dvrockslope9_912";
		obj.xpos = xpos;
		obj.ypos = ypos;
		obj.sprite = dvrockslope9_912;
		obj.colliderReferenceObject = dvrockslope9_912_collider;
		return obj;
	}
"""

        # Write ObjectCreate methods
        for obj_name, sprite_file in mapping.items():
            altered_function = sample_object_create_method_text.replace("create_dvrockslope9_912", obj_name)
            obj_name_no_create = obj_name.replace("create_", "")
            altered_function = sample_object_create_method_text.replace("dvrockslope9_912", obj_name_no_create)
            output_file.write(altered_function)

        output_file.write("}\n\n")

# Usage convert_spawn_list('path/to/input/spawn_list.txt', 'path/to/output/fp2_spawn_list.cs')

if __name__ == "__main__":
    print('Usage: python3 convert_spawn_list.py <input_file_path> <output_file_path>')
    print('Reminder: If you are using this for a Freedom Planet 1 Level Port, ')
    print('Reminder: You should confirm the player owns the game by checking Assets.dat ')
    input_file = sys.argv[1]
    mapping_file_path = sys.argv[2]
    output_dir = sys.argv[3]
    convert_spawn_list(input_file, mapping_file_path, output_dir)
