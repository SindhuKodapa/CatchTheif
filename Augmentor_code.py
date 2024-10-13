import Augmentor
import os
import shutil
from PIL import Image

# Path to your input image and the directory to save the augmented images
input_image_path = 'Downloads/training_data/train_bus/'
output_dir = 'output_test_augmented_images_bus'

# Ensure the output directory exists, and clean it if it already has files
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Create a pipeline for data augmentation
p = Augmentor.Pipeline(source_directory=os.path.dirname(input_image_path), output_directory=output_dir)

# Define augmentation operations
p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
p.flip_left_right(probability=0.5)
p.flip_top_bottom(probability=0.5)
p.zoom_random(probability=0.5, percentage_area=0.8)
p.random_contrast(probability=0.5, min_factor=0.7, max_factor=1.3)
p.random_brightness(probability=0.5, min_factor=0.7, max_factor=1.3)
p.random_color(probability=0.5, min_factor=0.7, max_factor=1.3)
p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=8)

# Use the sample method to generate 30 augmented images and store in the internal Augmentor output folder
p.sample(5)

# Move generated images from Augmentor's default folder to your specified output directory
generated_images_path = output_dir
for image_file in os.listdir(generated_images_path):
    image_path = os.path.join(generated_images_path, image_file)
    if os.path.isfile(image_path):
        shutil.move(image_path, os.path.join(output_dir, image_file))

# Clean up Augmentor's temporary folder
shutil.rmtree(generated_images_path)

print(f"Augmented images saved in {output_dir}")
