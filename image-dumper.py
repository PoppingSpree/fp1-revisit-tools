import os
import sys
import struct
import zlib
from PIL import Image  # Use Pillow for image handling

def read_image_data(f, offset):
    f.seek(offset)
    print(f"Current file position after seek: {f.tell()}")

    # Read image metadata
    width, height = struct.unpack('<HH', f.read(4))
    hot_x, hot_y = struct.unpack('<hh', f.read(4))
    if use_funky_image_encode:
        act_x, act_y = struct.unpack('<hh', f.read(4))
    else:
        act_x, act_y = (None, None)

    print(f"w: {width}, h: {height}, hx: {hot_x}, hy: {hot_y}")
    print(f"ax: {act_x}, ay: {act_y}")
    print(f"Current file position before size: {f.tell()}")

    # Read the size of the PNG data
    size = struct.unpack('<I', f.read(4))[0]
    print(f"PNG data size: {size}")

    # Read PNG data
    png_data = f.read(size)

    # Verify PNG signature
    png_signature = png_data[:8]
    print(f"PNG signature: {[hex(b) for b in png_signature]}")

    # Verify PNG footer (IEND chunk)
    png_footer = png_data[-12:]
    print(f"PNG footer: {[hex(b) for b in png_footer]}")

    return width, height, png_data

def convert_to_png(width, height, image_data, output_path):
    with open(output_path, 'wb') as png_file:
        png_file.write(image_data)


# Only use this version if we confirmed the png headers in the image data.
def convert_to_png_known(width, height, image_data, output_path):
    with open(output_path, 'wb') as png_file:
        png_file.write(image_data)

# Only use this version if we think we have raw bitmap data.
def convert_to_png_funky(width, height, image_data, output_path):
    image = Image.frombytes("RGBA", (width, height), image_data)
    image.save(output_path, 'PNG')

def estimate_image_count(f):
    f.seek(0)
    temp_data = f.read();
    png_signature = b"\x89\x50\x4E\x47"
    handle_size = 2  # Size of image handle in bytes
    offset_size = 4  # Size of image offset in bytes

    # Find the first occurrence of the PNG signature
    first_png_start = temp_data.find(png_signature)
    # print(f"data: {data}")
    print(f"png_signature: {png_signature}")
    print(f"first_png_start: {first_png_start}")

    if first_png_start == -1:
        print("No PNG signature found???");
        return None  # No PNG signature found

    # Subtract the metadata size (12 bytes that likely contain width, height, anchor, and data size.)
    table_end_point = first_png_start - 12 # Maybe should be 16 if we have to also back off the png portion?
    print(f"table_end_point ({table_end_point}) = first_png_start - 12 ({first_png_start} - 12)")

    # Estimate the number of images based on the handle and offset sizes
    estimated_images = table_end_point // (handle_size + offset_size)

    return estimated_images


def extract_images(asset_file_path, known_image_count, output_dir):
    with open(asset_file_path, "rb") as f:
        # Calculate offset table start (2 bytes per image handle + 2 bytes per image offset)
        offset_table_start = 0

        # Let's assume there are 16867 images and split up the handles and offsets accordingly.
        expected_image_count = 16867 # PC Retail seems to be 17162?
        if (known_image_count > 0):
            print(f"Image count given on command line: {known_image_count}")
            expected_image_count = known_image_count
        print(f"Initial assumed image count: {expected_image_count}")
        # expected_image_count = estimate_image_count(f)
        # print(f"Guestimated image count: {expected_image_count}")

        # Right now, we're hard-coding the expected image count.
        # We can probably guess this actual value for an arbitrary assets.dat
        # by searching for the first case of the png header in the file
        # then using a little bit of math: Subtract bits for the size and anchor,
        # Then divide the remaining data that we've read past by the number of bytes needed for
        # the handle and offset. The result should be the number of images.

        print(f"---Expecting {expected_image_count} handles---: ")

        for x in range(expected_image_count):
            # Read image offset from offset table (number of bytes)
            f.seek(offset_table_start)
            handle_value = struct.unpack("<H", f.read(2))[0] * 2  # Read 2 bytes as unsigned short and multiply by 2
            print(handle_value)
            offset_table_start += 2

        print(f"---Expecting {expected_image_count} offsets---: ")

        all_offsets = []
        for x in range(expected_image_count):
            # Read image offset from offset table (number of bytes)
            # f.seek(offset_table_start)
            image_offset = struct.unpack("<I", f.read(4))[0]  # Read 4 bytes as signed int
            print(image_offset)
            all_offsets.append(image_offset)
            # offset_table_start += 4

        print("We can assume if we see the hex '50 4E47' in the hex editor, that is the PNG header.")
        print("We can also reasonably assume that if we're at the PNG header, the size and other meta data rougly ")
        print("fills the ((2 * 6) + 4) = 16 bytes in front of it. ")
        print("Also seems like this PNG data section always ends with the same thing too?")
        # Some reference cases: 1000 3000 2000 2000 D402 0000 8950 4E47
        # (4945 4E44 AE42 6082) 0000 1F00 0000 3000 0805 0000 8950 4E47
        # (4945 4E44 AE42 6082) 1C00 2300 0000 0000 AE05 0000 8950 4E47

        # Seems a bit funky. My best guess for PS4: 
        # 4000 4000 1000 3000 2000 2000 BE00 0000 78
        # ...???
        # (F8 051F 6306 0530 0032 00)  1C 0023 0000 0000 004C 0200 0078 01ED D7


        # My best guess for PC Retail:
        # 4000 4000 1000 3000 2000 2000 3C02 0000
        # (F838 30FF A000 2000) 0000 1F00 0000 3000 C004 0000 BC04 0000
        # (402C 38FF 3000 3200) 1C00 2300 0000 0000 5804 0000 5404 0000


        # print("Only the first 10 are fine.")
        #
        # for image_index, image_offset in enumerate(all_offsets[0:10]):
        #     print(f"Processing image {image_index} at offset {image_offset}")
        #     width, height, image_data = read_image_data(f, image_offset)
        #     output_path = os.path.join(output_dir, f"{image_index}.png")
        #     print(f"Attempting to write image: {output_path}")
        #     convert_to_png(width, height, image_data, output_path)
        # print("Survived the initial test. Trying to extract all images...")


        print("Processing All Images:")

        for image_index, image_offset in enumerate(all_offsets):
            print(f"\nProcessing image {image_index} at offset {image_offset}")
            try:
                width, height, image_data = read_image_data(f, image_offset)
                output_path = os.path.join(output_dir, f"fp1-img-{image_index}.png")
                print(f"Attempting to write image: {output_path}")
                if (dry_run):
                    print(f"Dry Run will NOT write: {output_path}")
                elif (use_funky_image_encode):
                    convert_to_png_funky(width, height, image_data, output_path)
                    print(f"Successfully wrote image: {output_path}")
                else:
                    convert_to_png(width, height, image_data, output_path)
                    print(f"Successfully wrote image: {output_path}")
            except Exception as e:
                print(f"Error processing image {image_index}: {str(e)}")
                continue  # Move to the next image if there's an error
            if (early_end_value > 0 and image_index >= early_end_value):
                print(f"Ending early as requested.")
                break

        print("Finished processing all images.")

        print("That's all, folks!")

if __name__ == "__main__":
    usage_message = """Usage: python script_name.py [options]

Options:
  --use-funky-image-encode    Use alternative image encoding method
  --dry-run                   Perform a dry run without writing files
  --image-count <number>      Specify the number of images to extract
  --early-end <number>        Specify the number of images to extract

Examples:
  python script_name.py
  python script_name.py --use-funky-image-encode
  python script_name.py --dry-run
  python script_name.py --image-count 1000
  python script_name.py --early-end 10

Note:
- The script expects an 'Assets.dat' file in the current directory.
- Extracted images will be saved in a './images' directory.
- If no options are specified, the script will attempt to extract all images using default settings.
- Defaults to assuming the Assets.dat file has 16867 images."""

    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print(usage_message)  # Define usage_message with the above text
        sys.exit(0)

    use_funky_image_encode = "--use-funky-image-encode" in sys.argv
    dry_run = "--dry-run" in sys.argv
    known_image_count = "--image-count" in sys.argv
    early_end = "--early-end" in sys.argv

    known_image_count_value = -1
    early_end_value = -1

    if known_image_count:
        known_image_count_index = sys.argv.index("--image-count") + 1
        known_image_count_value = int(sys.argv[known_image_count_index])
    if early_end:
        early_end_index = sys.argv.index("--early-end") + 1
        early_end_value = int(sys.argv[early_end_index])

    asset_file_path = "./Assets.dat"
    output_dir = "./images"
    os.makedirs(output_dir, exist_ok=True)

    # Example: Extract a specific image (image ID 100)
    extract_images(asset_file_path, known_image_count_value, output_dir)

    # ... (You can call this for other image IDs based on your needs)