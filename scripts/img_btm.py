from pathlib import Path
from PIL import Image
import sys

def find_img_bottom(im):
    """Return the y-coordinate of the lowest point in an image containing
    non-transparent pixels"""
    width, height = im.size

    for y in range(height - 1, -1, -1):  # Iterate from bottom to top
        for x in range(width):
            pixel = im.getpixel((x, y))

            if not all(val == 0 for val in pixel):
                return y


def find_all_img_bottoms(dir_path):
    path = Path(dir_path)

    for item in path.iterdir(): # Iterate directly over items in the directory
        if item.is_file():
            ext = item.suffix.lower() # Get the file extension (e.g., '.png')
            if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
                im = Image.open(item)
                print(f"file {item} : {find_img_bottom(im)}")

if __name__ == '__main__':
    find_all_img_bottoms(sys.argv[1])