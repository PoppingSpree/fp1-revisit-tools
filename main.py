import os
import subprocess
import sys


def call_script(script_path, in_file, out_folder, num_retries=3):
    # out_file = os.path.join(out_folder, os.path.splitext(os.path.basename(in_file))[0])
    for i in range(num_retries):
        try:
            subprocess.run(['python', script_path, in_file, out_folder], check=True)
            return  # If we reach this line, no error was raised, so break out of loop.
        except subprocess.CalledProcessError:
            if i < num_retries - 1:  # i is zero indexed
                continue
            else:
                with open('logfile.log', 'a') as f:
                    f.write(f"Script {script_path} failed on file {in_file} after {num_retries} retries\n")
                return


def modify_and_move_tokens_file(in_file, out_folder):
    out_file = os.path.join(out_folder, os.path.basename(in_file))
    with open(in_file, 'r') as src, open(out_file, 'w') as dest:
        tokens = [line.strip() for line in src]
        dest.write(' '.join(tokens))


def call_parse_cpp(script_path, cpp_folder, tokens_dir, out_folder):
    for filename in os.listdir(tokens_dir):
        filepath = os.path.join(tokens_dir, filename)

        # Adjust the filename
        base_name = os.path.splitext(filename)[0]  # Get the base name from the input file
        new_filename = base_name.replace("_init_tokens",
                                         "_mappings") + '.txt'  # Replace part of the base name and add file extension

        out_file = os.path.join(out_folder, new_filename)  # Set out_file with the new filename
        subprocess.run(['python', script_path, cpp_folder, out_file, '--file', filepath], check=True)



def main():
    print("Usage: python main.py [--skip-spawns] [--skip-tokens] [--skip-mappings] [--skip-unity]")
    skip_spawns = "--skip-spawns" in sys.argv
    skip_tokens = "--skip-tokens" in sys.argv
    skip_mappings = "--skip-mappings" in sys.argv
    skip_unity = "--skip-unity" in sys.argv

    work_dir = "work"
    cpp_folder = os.path.join(work_dir, "c")
    spawn_folder = os.path.join(work_dir, "spawnlists")
    tokens_folder = os.path.join(work_dir, "tokens")
    mappings_folder = os.path.join(work_dir, "mappings")
    unity_folder = os.path.join(work_dir, "unity")

    if skip_spawns:
        print("Skipping generation of frame init spawnlists...")
        # skip the functionality here
    else:
        for filename in os.listdir(cpp_folder):
            if filename.endswith('.cpp'):
                filepath = os.path.join(cpp_folder, filename)
                call_script("extract_frame_init.py", filepath, spawn_folder)

    if skip_tokens:
        print("Skipping generation of object token lists...")
        # skip the functionality here
    else:
        for filename in os.listdir(spawn_folder):
            filepath = os.path.join(spawn_folder, filename)
            call_script("extract_tokens.py", filepath, tokens_folder)

    if skip_mappings:
        print("Skipping generation of object to image mappings...")
        # skip the functionality here
    else:
        for filename in os.listdir(tokens_folder):
            filepath = os.path.join(tokens_folder, filename)
        call_parse_cpp("parse_cpp_files.py", cpp_folder, tokens_folder, mappings_folder)

    if skip_unity:
        print("Skipping generation of Unity-style MonoBehavior spawnlists")
        # skip the functionality here
    else:
        for filename in os.listdir(spawn_folder):
            filepath = os.path.join(spawn_folder, filename)
            base_name = filename.replace("_init.txt", "")  # Get the base name from the input file
            out_filename = 'fp1_' + base_name + '.cs'
            out_filepath = os.path.join(unity_folder, out_filename)
            call_script("convert_spawn_list.py", filepath, out_filepath)

if __name__ == "__main__":
    main()
