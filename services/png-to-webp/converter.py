from PIL import Image
import os

input_folder = 'inputs'
output_folder = 'outputs'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of PNG files in the input folder
png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

for png_file in png_files:
    # Open the PNG file
    png_path = os.path.join(input_folder, png_file)
    with Image.open(png_path) as img:
        # Convert the image to WebP format
        webp_file = os.path.splitext(png_file)[0] + '.webp'
        webp_path = os.path.join(output_folder, webp_file)
        img.save(webp_path, 'webp')
        print(f"Converted {png_file} to {webp_file}.")

print("Conversion complete.")
