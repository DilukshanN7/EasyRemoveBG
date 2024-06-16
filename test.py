import sys
import os
from rembg import remove
from PIL import Image
from io import BytesIO

file_path = sys.argv[1]

folder_path = os.path.dirname(file_path)

try:
    with open(file_path, 'rb') as file:
        input_bytes = file.read()

    output_bytes = remove(input_bytes)

    original_basename = os.path.basename(file_path)
    name_without_ext = os.path.splitext(original_basename)[0]
    new_image_path = os.path.join(folder_path, 'rembg_' + name_without_ext + '.png')

    result_image = Image.open(BytesIO(output_bytes))
    result_image.save(new_image_path, format='PNG')
except Exception as e:
    print(f"Error processing file: {e}")
