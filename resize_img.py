# from PIL import Image
#
# # Path to your input image
# input_path = "results/young_man1.jpg"
# # Path to save the resized image
# output_path = "results/young_man1_resized.jpg"
#
# # Open the image
# image = Image.open(input_path)
#
# # Resize to 1024x1024 (using high-quality resampling)
# resized_image = image.resize((1024, 1024), Image.LANCZOS)
#
# # Save the resized image
# resized_image.save(output_path)
#
# print(f"Image saved to {output_path}")

# from PIL import Image
#
# # Path to your input image
# input_path = "path_figure/young_man4.jpg"
# # Path to save the cropped image
# output_path = "path_figure/young_man4_cropped.jpg"
#
# # Open the image
# image = Image.open(input_path)
# width, height = image.size
#
# print(width, height)
# # Calculate coordinates for center crop
# left = (width - 1024) / 2
# top = (height - 1024) / 2
# right = (width + 1024) / 2
# bottom = (height + 1024) / 2
#
#
#
#
# # Crop the center
# cropped_image = image.crop((left, top, right, bottom))
#
# if cropped_image.mode == "RGBA":
#     cropped_image = cropped_image.convert("RGB")
# # Save the cropped image
# cropped_image.save(output_path)
#
# print(f"Cropped image saved to {output_path}")


from PIL import Image

# Path to your input image
input_path = "patch_figure_variations/young_man5.jpg"
# Path to save the cropped image
output_path = "patch_figure_variations/young_man5_cropped.png"

# Open the image
image = Image.open(input_path)
width, height = image.size

print(f"Original size: {width}x{height}")

# Desired crop size
crop_width = 1650
crop_height = 1650

# Calculate coordinates for upper-center crop
left = (width - crop_width) / 2  + 500     # center horizontally
top = 0 + 300                               # start from the top
right = (width + crop_width) / 2 + 100
bottom = crop_height + 150                 # crop downward from the top

# Crop the upper-center region
cropped_image = image.crop((left, top, right, bottom))

# Convert to RGB if necessary
if cropped_image.mode == "RGBA":
    cropped_image = cropped_image.convert("RGB")

# Save the cropped image
cropped_image.save(output_path)

print(f"Cropped (upper-center) image saved to {output_path}")