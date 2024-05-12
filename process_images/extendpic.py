from PIL import Image

def extend_image(image_path, output_path, extra_width, extra_height):
    # Open the original image
    with Image.open(image_path) as img:
        # Calculate the new dimensions
        new_width = img.width + extra_width
        new_height = img.height + extra_height

        # Create a new image with the extended size and the same mode
        new_img = Image.new(img.mode, (new_width, new_height))

        # Paste the original image into the center of the new image
        new_img.paste(img, (extra_width // 2, extra_height // 2))

        # Fill in the extended areas by replicating the nearest edge pixels

        # Fill vertical sides
        for y in range(new_img.height):
            for x in range(extra_width // 2):  # Left side
                new_img.putpixel((x, y), new_img.getpixel((extra_width // 2, y)))
            for x in range(new_img.width - extra_width // 2, new_img.width):  # Right side
                new_img.putpixel((x, y), new_img.getpixel((new_img.width - extra_width // 2 - 1, y)))

        # Fill horizontal sides
        for x in range(new_img.width):
            for y in range(extra_height // 2):  # Top side
                new_img.putpixel((x, y), new_img.getpixel((x, extra_height // 2)))
            for y in range(new_img.height - extra_height // 2, new_img.height):  # Bottom side
                new_img.putpixel((x, y), new_img.getpixel((x, new_img.height - extra_height // 2 - 1)))

        # Save the extended image
        new_img.save(output_path)
        print(f"Extended image saved to {output_path}")

# Example usage
# Example usage
image_path = './img/download.jpeg'  # Replace with your image's path
output_path = 'extended_image.jpg'
extend_image(image_path, output_path, 100, 100)  # Extend by 100px on each side
