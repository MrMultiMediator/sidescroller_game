from pathlib import Path
from PIL import Image
import sys

def scale(im, sf_x, sf_y):
    "Scale a PIL Image by sf_x and sf_y."
    width, height = im.size

    new_width = int(width * sf_x)
    new_height = int(height * sf_y)

    return im.resize((new_width, new_height))

def scale_all_imgs_in_dir(sf, dir_path):
    path = Path(dir_path)

    for item in path.iterdir(): # Iterate directly over items in the directory
        if item.is_file():
            ext = item.suffix.lower() # Get the file extension (e.g., '.png')
            if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
                im = Image.open(item)
                im2 = scale(im, sf, sf)
                im2.save(item)

if __name__ == '__main__':
    dir_path = sys.argv[1]

    sf = float(sys.argv[2])

    scale_all_imgs_in_dir(sf, dir_path)