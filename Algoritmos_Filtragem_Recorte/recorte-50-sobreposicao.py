import math
import os
from PIL import Image

def tile_image_with_overlap(image_path, tile_size, output_dir, overlap_ratio=0.5):

    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(image_path)
    width, height = img.size

    stride = int(tile_size * (1 - overlap_ratio))  

    n_x = math.ceil((width - tile_size) / stride) + 1
    n_y = math.ceil((height - tile_size) / stride) + 1

    os.makedirs(output_dir, exist_ok=True)

    for i in range(n_y):
        for j in range(n_x):
            left = j * stride
            upper = i * stride
            right = left + tile_size
            lower = upper + tile_size

            tile = img.crop((left, upper, right, lower))
            tile = tile.convert("RGB")

            padded_tile = Image.new("RGB", (tile_size, tile_size), (0, 0, 0))
            padded_tile.paste(tile, (0, 0))

            tile_filename = f"tile_{i}_{j}.png"
            padded_tile.save(os.path.join(output_dir, tile_filename))


if __name__ == "__main__":
    image_path = r"C:\Users\mfreq\Desktop\UTAD\Semestre 2\LPEI\fase2\QGIS\13-5-5.tif"
    tile_size = 512
    output_dir = "13-5-5-recortada"
    tile_image_with_overlap(image_path, tile_size, output_dir)
