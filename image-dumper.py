import os
import struct
import zlib
from PIL import Image  # Use Pillow for image handling

def extract_image_ai_generated(asset_file_path, image_id, output_dir):
    with open(asset_file_path, "rb") as f:
        # Calculate offset table start (2 bytes per image handle + 2 bytes per image offset)
        offset_table_start = 2 * image_id * 2 + 2 * 16893 * 2

        # Read image offset from offset table
        f.seek(offset_table_start)
        image_offset = struct.unpack("<H", f.read(2))[0] * 2  # Read 2 bytes as unsigned short and multiply by 2

        # Read image data
        f.seek(image_offset)
        hotspot_x, hotspot_y, act_x, act_y = struct.unpack("<hhhh", f.read(8))
        # If 3ds: _, target_format = struct.unpack("<B", f.read(1))  # Uncomment for 3ds
        size = struct.unpack("<I", f.read(4))[0]
        compressed_data = f.read(size)

        # Decompress image data
        image_data = zlib.decompress(compressed_data)

        # Create image object
        image = Image.frombytes("RGBA", (128, 128), image_data)  # Assuming RGBA format, adjust if needed

        # Save image
        image_path = os.path.join(output_dir, f"{image_id}.png")
        image.save(image_path)

def read_image_data_funky(f, offset):
    f.seek(offset)
    print(f"Current file position after seek: {f.tell()}")

    # Read image metadata
    width, height = struct.unpack('<HH', f.read(4))
    hot_x, hot_y = struct.unpack('<hh', f.read(4))

    print(f"w: {width}, h: {height}, hx: {hot_x}, hy: {hot_y}")
    print(f"Current file position before reading size: {f.tell()}")

    # Unlike mot other situatinos, this size was written with writeIntString
    # def writeIntString(self, value):
    #     self.writeInt(len(value), True) # This is the size of the data portion.
    #     self.write(value) # This is the actual data.



    # Read compressed data size
    size_bytes = f.read(4)
    print(f"Size bytes: {[hex(b) for b in size_bytes]}")
    data_size = struct.unpack('<I', size_bytes)[0]
    print(f"data_size: {data_size}")

    # Read and decompress the image data
    compressed_data = f.read(data_size)
    image_data = zlib.decompress(compressed_data)

    return width, height, image_data


def read_image_data(f, offset):
    f.seek(offset)
    print(f"Current file position after seek: {f.tell()}")

    # Read image metadata
    width, height = struct.unpack('<HH', f.read(4))
    hot_x, hot_y = struct.unpack('<hh', f.read(4))

    print(f"w: {width}, h: {height}, hx: {hot_x}, hy: {hot_y}")
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


def convert_to_png_funky(width, height, image_data, output_path):
    image = Image.frombytes("RGBA", (width, height), image_data)
    image.save(output_path, 'PNG')


def extract_images(asset_file_path, image_id, output_dir):
    with open(asset_file_path, "rb") as f:
        # Calculate offset table start (2 bytes per image handle + 2 bytes per image offset)
        offset_table_start = 0

        # Let's assume there are 16867 images and split up the handles and offsets accordingly.

        print("Expecting 16867 handles: ")

        for x in range(16867):
            # Read image offset from offset table (number of bytes)
            f.seek(offset_table_start)
            handle_value = struct.unpack("<H", f.read(2))[0] * 2  # Read 2 bytes as unsigned short and multiply by 2
            print(handle_value)
            offset_table_start += 2

        print("Expecting 16867 offsets: ")

        all_offsets = []
        for x in range(16867):
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
                convert_to_png(width, height, image_data, output_path)
                print(f"Successfully wrote image: {output_path}")
            except Exception as e:
                print(f"Error processing image {image_index}: {str(e)}")
                continue  # Move to the next image if there's an error

        print("Finished processing all images.")

        print("That's all, folks!")

if __name__ == "__main__":
    asset_file_path = "./Assets.dat"
    output_dir = "./images"
    os.makedirs(output_dir, exist_ok=True)

    # Example: Extract a specific image (image ID 100)
    extract_images(asset_file_path, 100, output_dir)

    # ... (You can call this for other image IDs based on your needs)