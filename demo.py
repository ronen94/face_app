import os
from PIL import Image

def flip_images(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Supported image file extensions
    valid_ext = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        # Process only files with supported image extensions
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in valid_ext:
            image = Image.open(file_path)
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

            # Save the flipped image to the output directory
            output_path = os.path.join(output_dir, filename)
            flipped_image.save(output_path)
            print(f"Flipped and saved: {output_path}")

if __name__ == "__main__":
    input_directory = "C:/Users/ronen/projects/face_app/assets/right_ear"
    output_directory = "C:/Users/ronen/projects/face_app/assets/left_ear"
    flip_images(input_directory, output_directory)