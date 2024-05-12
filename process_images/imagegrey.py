from PIL import Image
import os

def convert_images_to_grayscale(folder_path, output_folder_path):
    # Ensure the output directory exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    # Loop through all files in the folder
    for img_file in os.listdir(folder_path):
        if img_file.endswith(('.png', '.jpg', '.jpeg')):
            # Open the image file
            img_path = os.path.join(folder_path, img_file)
            with Image.open(img_path) as img:
                # Convert the image to grayscale
                grayscale_img = img.convert('L')

                # Save the grayscale image to the output directory
                output_path = os.path.join(output_folder_path, f"gray_{img_file}")
                grayscale_img.save(output_path)
                print(f"Converted and saved: {output_path}")

# Example usage
folder_path = './img/'  # Replace with the path to your images folder
output_folder_path = './outputimg/'  # Replace with the path where you want to save the grayscale images
convert_images_to_grayscale(folder_path, output_folder_path)
