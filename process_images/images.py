from PIL import Image
import os

def combine_images(folder_path, output_path):
    images = [Image.open(os.path.join(folder_path, img)) for img in os.listdir(folder_path) if img.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        raise ValueError("No images found in the directory")

    # Set the number of columns
    cols = 2
    rows = (len(images) + 1) // cols  # Calculate the number of rows needed

    # Determine the maximum image width and height in the list
    max_width = max(image.size[0] for image in images)
    max_height = max(image.size[1] for image in images)

    # Create a new image with a white background
    combined_image = Image.new('RGB', (cols * max_width, rows * max_height), 'white')
    
    # Paste images
    for index, image in enumerate(images):
        x = index % cols * max_width
        y = index // cols * max_height
        # Resize image to max width and height using LANCZOS resampling for high quality
        image = image.resize((max_width, max_height), Image.Resampling.LANCZOS)
        combined_image.paste(image, (x, y))
    
    # Save the combined image
    combined_image.save(output_path)
    print(f"Image saved to {output_path}")

# Example usage:

# Example usage:
folder_path = './img/'  # Update this path
output_path = 'combined_image.jpg'
combine_images(folder_path, output_path)
