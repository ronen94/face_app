import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path
from datetime import datetime

WORKDIR = Path(__file__).parent


class CatalogEditor:
    def __init__(self):
        self.base_image = None
        self.overlays = []
        self.selected_feature = None
        self.selected_category = "eyes"
        self.current_scale = 0.2
        self.current_rotation = 0
        self.current_opacity = 1.0
        self.feature_catalog = {}
        self.preview_overlay = None
        self.init_feature_catalog()

    def add_to_catalog(self, category: str, folder: Path):
        self.feature_catalog[category] = {}
        if folder.exists():
            for img_file in folder.glob("*.png"):
                try:
                    # Use filename without extension as the label
                    name = img_file.stem.replace("_", " ").title()
                    img = Image.open(img_file).convert("RGBA")

                    # remove white background
                    datas = img.getdata()
                    new_data = []
                    for r, g, b, a in datas:
                        # turn nearly-white pixels into transparent
                        if r + g + b > 650:
                            new_data.append((255, 255, 255, 0))  # transparent
                        else:
                            new_data.append((r, g, b, a))
                    img.putdata(new_data)

                    self.feature_catalog[category][name] = img
                    print(f"✓ Loaded: {name} from {img_file.name}")
                except Exception as e:
                    print(f"✗ Failed to load {img_file.name}: {e}")

    def init_feature_catalog(self):
        """Initialize catalog - loads both synthetic and real images"""

        # EYES - Real Images (your images)
        self.feature_catalog['eyes'] = {}

        # Try to load real eye images from assets folder
        eyes_folder = WORKDIR / "assets" / "eye_images"
        if eyes_folder.exists():
            for img_file in eyes_folder.glob("*.png"):
                try:
                    img = Image.open(img_file).convert("RGBA")
                    # Use filename without extension as the label
                    name = img_file.stem.replace("_", " ").title()
                    self.feature_catalog['eyes'][name] = img
                    print(f"✓ Loaded: {name} from {img_file.name}")
                except Exception as e:
                    print(f"✗ Failed to load {img_file.name}: {e}")

        mustahce_folder = WORKDIR / "assets" / "mustache_images"
        self.add_to_catalog('mustache', mustahce_folder)

        eyeglasses_folder = WORKDIR / "assets" / "eyeglasses"
        self.add_to_catalog('eyeglasses', eyeglasses_folder)

        left_eyebrow_folder = WORKDIR / "assets" / "left_eyebrow"
        self.add_to_catalog('left_eyebrow', left_eyebrow_folder)

        right_eyebrow_folder = WORKDIR / "assets" / "right_eyebrow"
        self.add_to_catalog('right_eyebrow', right_eyebrow_folder)

        lips_folder = WORKDIR / "assets" / "lips"
        self.add_to_catalog('lips', lips_folder)

        nose_folder = WORKDIR / "assets" / "nose_images"
        self.add_to_catalog('nose', nose_folder)

        # If no images found, create a placeholder
        if not self.feature_catalog['eyes']:
            print("⚠ No eye images found in assets/eye_images/")
            placeholder = Image.new('RGBA', (200, 100), (200, 200, 200, 255))
            draw = ImageDraw.Draw(placeholder)
            draw.text((100, 50), "No images\nfound", fill=(100, 100, 100, 255), anchor="mm")
            self.feature_catalog['eyes']['Placeholder'] = placeholder

        # BEARD VARIATIONS (synthetic for testing)
        self.feature_catalog['beard'] = {}

        beard1 = Image.new('RGBA', (180, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard1)
        draw.ellipse([30, 20, 150, 120], fill=(45, 28, 18, 220))
        draw.ellipse([40, 10, 140, 100], fill=(55, 35, 22, 200))
        self.feature_catalog['beard']['Full Beard'] = beard1

        beard2 = Image.new('RGBA', (120, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard2)
        draw.ellipse([30, 30, 90, 90], fill=(45, 28, 18, 220))
        draw.rectangle([45, 10, 75, 50], fill=(45, 28, 18, 220))
        self.feature_catalog['beard']['Goatee'] = beard2

    def create_catalog_gallery(self, category):
        """Create a gallery of thumbnails for the selected category"""
        if category not in self.feature_catalog:
            return None

        items = self.feature_catalog[category]
        gallery_items = []

        for name, img in items.items():
            # Create a thumbnail with white background
            thumb_size = (150, 150)
            thumbnail = Image.new('RGBA', thumb_size, (255, 255, 255, 255))

            # Paste the feature in the center
            img_copy = img.copy()
            img_copy.thumbnail((120, 120), Image.Resampling.LANCZOS)

            # Center the image
            x = (thumb_size[0] - img_copy.width) // 2
            y = (thumb_size[1] - img_copy.height) // 2
            thumbnail.paste(img_copy, (x, y), img_copy)

            # Add label
            draw = ImageDraw.Draw(thumbnail)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
            except:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (thumb_size[0] - text_width) // 2
            draw.text((text_x, 5), name, fill=(0, 0, 0, 255), font=font)

            gallery_items.append((thumbnail, name))

        return gallery_items

    def get_feature_preview(self):
        """Generate a preview of the currently selected feature with current settings"""
        if self.selected_feature is None:
            # Return a placeholder
            placeholder = Image.new('RGBA', (300, 300), (240, 240, 240, 255))
            draw = ImageDraw.Draw(placeholder)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
            except:
                font = ImageFont.load_default()
            text = "Select a feature\nfrom catalog"
            draw.text((150, 150), text, fill=(150, 150, 150, 255), font=font, anchor="mm")
            return placeholder

        category, feature_name = self.selected_feature

        # Get the original image from catalog
        if category not in self.feature_catalog or feature_name not in self.feature_catalog[category]:
            return self.get_feature_preview()  # Return placeholder if not found

        feature_img = self.feature_catalog[category][feature_name].copy()

        # Apply current transformations
        if self.current_scale != 1.0:
            new_size = (int(feature_img.width * self.current_scale),
                        int(feature_img.height * self.current_scale))
            feature_img = feature_img.resize(new_size, Image.Resampling.LANCZOS)

        if self.current_rotation != 0:
            feature_img = feature_img.rotate(self.current_rotation, expand=True,
                                             resample=Image.Resampling.BICUBIC)

        if self.current_opacity != 1.0:
            feature_array = np.array(feature_img)
            if feature_array.shape[2] == 4:  # Has alpha channel
                feature_array[:, :, 3] = (feature_array[:, :, 3] * self.current_opacity).astype(np.uint8)
                feature_img = Image.fromarray(feature_array)

        # Create a canvas that fits the feature with padding
        # Make canvas size adaptive to always show the entire feature
        canvas_size = 400  # Larger base canvas
        padding = 20

        # If feature is larger than canvas, scale it down to fit
        max_feature_size = canvas_size - (2 * padding)
        if feature_img.width > max_feature_size or feature_img.height > max_feature_size:
            # Scale down to fit while maintaining aspect ratio
            feature_img.thumbnail((max_feature_size, max_feature_size), Image.Resampling.LANCZOS)

        # Create white background canvas
        canvas = Image.new('RGBA', (canvas_size, canvas_size), (255, 255, 255, 255))

        # Center the feature on the canvas
        x = (canvas_size - feature_img.width) // 2
        y = (canvas_size - feature_img.height) // 2
        canvas.paste(feature_img, (x, y), feature_img)

        # Add a reference grid to show scale
        draw = ImageDraw.Draw(canvas)

        # Draw a light border around the feature to show its bounds
        border_rect = [x - 1, y - 1, x + feature_img.width, y + feature_img.height]
        draw.rectangle(border_rect, outline=(200, 200, 200, 255), width=1)

        # Add size info at the bottom
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            font = ImageFont.load_default()

        size_text = f"Size: {self.current_scale:.1f}x ({feature_img.width}×{feature_img.height}px)"
        text_bbox = draw.textbbox((0, 0), size_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw.text(((canvas_size - text_width) // 2, canvas_size - 25),
                  size_text, fill=(100, 100, 100, 255), font=font)

        return canvas

    def get_current_display_image(self):
        """Get the current image that should be displayed (with overlays if any)"""
        if self.base_image is None:
            return None
        # Return as numpy array since image_display expects numpy
        return np.array(self.composite_image())

    def change_category(self, category):
        """Handle category change - only update gallery, not the image"""
        gallery = self.create_catalog_gallery(category)
        # Return gr.update() to skip updating the image (no reload needed)
        return gr.update(), gallery

    def select_from_catalog(self, evt: gr.SelectData, category):
        """Handle selection from the catalog gallery with auto-confirm"""
        selected_name = evt.value['caption']

        # AUTO-CONFIRM: If there's a preview overlay active, confirm it first
        status_msg = ""
        image_update = gr.update()  # By default, don't update the image

        if self.preview_overlay is not None:
            # Automatically confirm the current preview
            self.overlays.append(self.preview_overlay)
            old_feature_name = self.preview_overlay['name']
            self.preview_overlay = None
            status_msg = f"✅ Auto-confirmed {old_feature_name}!\n"
            # Update the image to show the confirmed placement
            image_update = self.get_current_display_image()

        # Now select the new feature
        self.selected_feature = (category, selected_name)

        # Reset sliders to default when selecting new feature
        self.current_scale = 0.2
        self.current_rotation = 0
        self.current_opacity = 1.0

        preview_img = self.get_feature_preview()
        status_msg += f"✓ Selected: {selected_name} from {category}\n💡 Adjust size/rotation/opacity below and watch the preview update!"

        return (
            image_update,  # Only update if we auto-confirmed, otherwise skip
            status_msg,
            preview_img,
            0.2,  # Reset scale slider
            0,  # Reset rotation slider
            1.0  # Reset opacity slider
        )

    def handle_image_upload(self, img):
        """Handle image upload separately from clicks"""
        if img is None:
            return None, "❌ No image provided"

        # store as PIL and return numpy (image_display is set to type="numpy")
        self.base_image = Image.fromarray(img).convert('RGBA')
        self.overlays = []
        self.preview_overlay = None
        return np.array(
            self.base_image), "✓ Image loaded! Now select a feature from the catalog and click on the image to place it."

    def handle_image_click(self, img, evt: gr.SelectData):
        """Place or move the selected feature where the user clicked"""
        if img is None:
            return None, "❌ Please upload an image first"

        # Ensure base image is set
        if self.base_image is None:
            self.base_image = Image.fromarray(img).convert('RGBA')

        if self.selected_feature is None:
            return np.array(self.composite_image()), "❌ Please select a feature from the catalog first"

        category, feature_name = self.selected_feature
        feature_img = self.feature_catalog[category][feature_name].copy()

        # Get click coordinates - evt.index contains (x, y) pixel coordinates
        click_x = evt.index[0]
        click_y = evt.index[1]

        # If we have a preview overlay, we're moving it
        if self.preview_overlay is not None:
            self.preview_overlay['x'] = click_x
            self.preview_overlay['y'] = click_y
            result = self.composite_image()
            return np.array(
                result), f"🔄 Moved {feature_name} to ({click_x}, {click_y}). Click 'Confirm' or click again to adjust."
        else:
            # Create new preview overlay
            overlay_info = {
                'category': category,
                'name': feature_name,
                'x': click_x,
                'y': click_y,
                'scale': self.current_scale,
                'rotation': self.current_rotation,
                'opacity': self.current_opacity
            }
            self.preview_overlay = overlay_info
            result = self.composite_image()
            return np.array(
                result), f"✓ Preview: {feature_name} at ({click_x}, {click_y}). Click 'Confirm' to keep it, or click again to move it."

    def confirm_placement(self):
        """Confirm the current preview and add it to overlays"""
        if self.preview_overlay is None:
            return np.array(self.composite_image()) if self.base_image else None, "❌ No feature to confirm"

        self.overlays.append(self.preview_overlay)
        feature_name = self.preview_overlay['name']
        self.preview_overlay = None
        result = self.composite_image()
        return np.array(result), f"✅ Confirmed {feature_name}! Select another feature or adjust this one."

    def cancel_preview(self):
        """Cancel the current preview"""
        if self.preview_overlay is None:
            return np.array(self.composite_image()) if self.base_image else None, "❌ No preview to cancel"

        self.preview_overlay = None
        result = self.composite_image()
        return np.array(result), "↩️ Preview cancelled"

    def composite_image(self):
        """Composite all overlays onto the base image, including preview"""
        if self.base_image is None:
            return None

        result = self.base_image.copy()

        # First composite all confirmed overlays
        for overlay in self.overlays:
            result = self._apply_overlay(result, overlay)

        # Then add the preview overlay if it exists
        if self.preview_overlay is not None:
            result = self._apply_overlay(result, self.preview_overlay)

        return result

    def _apply_overlay(self, base_img, overlay):
        """Apply a single overlay to an image"""
        category = overlay['category']
        name = overlay['name']

        if category not in self.feature_catalog or name not in self.feature_catalog[category]:
            return base_img

        feature_img = self.feature_catalog[category][name].copy()

        # Apply transformations
        if overlay['scale'] != 1.0:
            new_size = (int(feature_img.width * overlay['scale']),
                        int(feature_img.height * overlay['scale']))
            feature_img = feature_img.resize(new_size, Image.Resampling.LANCZOS)

        if overlay['rotation'] != 0:
            feature_img = feature_img.rotate(overlay['rotation'], expand=True,
                                             resample=Image.Resampling.BICUBIC)

        if overlay['opacity'] != 1.0:
            feature_array = np.array(feature_img)
            if feature_array.shape[2] == 4:  # Has alpha channel
                feature_array[:, :, 3] = (feature_array[:, :, 3] * overlay['opacity']).astype(np.uint8)
                feature_img = Image.fromarray(feature_array)

        # Calculate position (center the feature at the clicked point)
        x = overlay['x'] - feature_img.width // 2
        y = overlay['y'] - feature_img.height // 2

        # Paste the feature
        base_img.paste(feature_img, (x, y), feature_img)

        return base_img

    def undo_last(self):
        """Remove the last added overlay or cancel preview"""
        if self.preview_overlay is not None:
            self.preview_overlay = None
            result = self.composite_image()
            return np.array(result), "↩️ Cancelled preview"

        if not self.overlays:
            return np.array(self.composite_image()) if self.base_image else None, "❌ Nothing to undo"

        self.overlays.pop()
        result = self.composite_image()
        return np.array(result), "✓ Undid last action"

    def clear_all(self):
        """Remove all overlays and preview"""
        self.overlays = []
        self.preview_overlay = None
        if self.base_image:
            return np.array(self.base_image), "✓ Cleared all features"
        return None, "✓ Cleared all features"

    def update_scale(self, scale):
        self.current_scale = scale

        if self.preview_overlay is not None:
            self.preview_overlay['scale'] = scale
            current_img = self.get_current_display_image()  # Update when preview exists
        else:
            current_img = gr.update()  # Skip update when just browsing catalog

        preview_img = self.get_feature_preview()
        return current_img, f"Scale: {scale:.2f}x", preview_img

    def update_rotation(self, rotation):
        """Update the current rotation setting and preview if active"""
        self.current_rotation = rotation

        # FIXED: Update preview overlay BEFORE getting the display image
        if self.preview_overlay is not None:
            self.preview_overlay['rotation'] = rotation

        # Now get the images with updated values
        preview_img = self.get_feature_preview()
        current_img = self.get_current_display_image()

        return current_img, f"Rotation: {rotation}°", preview_img

    def update_opacity(self, opacity):
        """Update the current opacity setting and preview if active"""
        self.current_opacity = opacity

        # FIXED: Update preview overlay BEFORE getting the display image
        if self.preview_overlay is not None:
            self.preview_overlay['opacity'] = opacity

        # Now get the images with updated values
        preview_img = self.get_feature_preview()
        current_img = self.get_current_display_image()

        return current_img, f"Opacity: {int(opacity * 100)}%", preview_img

    def get_overlay_list(self):
        """Get a formatted list of current overlays"""
        if not self.overlays and not self.preview_overlay:
            return "No features placed yet"

        overlay_text = "Confirmed Features:\n"
        if self.overlays:
            for i, overlay in enumerate(self.overlays, 1):
                overlay_text += f"{i}. {overlay['name']} ({overlay['category']})\n"
        else:
            overlay_text += "None\n"

        if self.preview_overlay:
            overlay_text += f"\n⏳ Preview: {self.preview_overlay['name']} (click Confirm or click again to move)"

        return overlay_text

    def save_image(self, save_path):
        """Save the final composite image to the specified path"""
        if self.base_image is None:
            return "❌ No image to save! Please upload an image first."

        # Check if there's a preview that needs to be confirmed
        if self.preview_overlay is not None:
            return "⚠️ You have an unconfirmed preview! Please click 'Confirm' or 'Cancel' before saving."

        # Validate and process the save path
        if not save_path or save_path.strip() == "":
            # Generate a default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"edited_image_{timestamp}.png"

        try:
            # Convert to Path object and resolve it
            save_path = Path(save_path).expanduser()

            # If it's a relative path, make it relative to WORKDIR
            if not save_path.is_absolute():
                save_path = WORKDIR / save_path

            # Create parent directories if they don't exist
            save_path.parent.mkdir(parents=True, exist_ok=True)

            # Get the composite image
            final_image = self.composite_image()

            # Determine format based on file extension
            file_ext = save_path.suffix.lower()

            if file_ext in ['.jpg', '.jpeg']:
                # Convert RGBA to RGB for JPEG (no transparency support)
                rgb_image = Image.new('RGB', final_image.size, (255, 255, 255))
                rgb_image.paste(final_image, mask=final_image.split()[3] if final_image.mode == 'RGBA' else None)
                rgb_image.save(save_path, 'JPEG', quality=95)
            elif file_ext == '.png' or file_ext == '':
                # Save as PNG (supports transparency)
                if file_ext == '':
                    save_path = save_path.with_suffix('.png')
                final_image.save(save_path, 'PNG')
            else:
                # Try to save with the specified format
                final_image.save(save_path)

            return f"✅ Image saved successfully to:\n{save_path.absolute()}"

        except PermissionError:
            return f"❌ Permission denied! Cannot write to:\n{save_path}\nPlease choose a different location or check your permissions."
        except Exception as e:
            return f"❌ Error saving image:\n{str(e)}\n\nPlease check the path and try again."


def create_interface():
    editor = CatalogEditor()

    with gr.Blocks(title="Feature Catalog Editor", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎨 Feature Catalog Editor - Real Image Support")
        gr.Markdown("Upload an image, select features from the catalog, and click on the image to place them!")
        gr.Markdown("💡 **NEW:** Real-time preview shows your exact size adjustments before placing!")

        with gr.Row():
            # Left column - Single Interactive Image
            with gr.Column(scale=2):
                image_display = gr.Image(
                    label="📤 Upload Image & Click to Place Features",
                    type="numpy",
                    interactive=True,
                    sources=["upload", "clipboard"]
                )

                with gr.Row():
                    confirm_btn = gr.Button("✅ Confirm Placement", variant="primary", size="sm")
                    cancel_btn = gr.Button("↩️ Cancel Preview", variant="secondary", size="sm")
                    undo_btn = gr.Button("↶ Undo Last", variant="secondary", size="sm")
                    clear_btn = gr.Button("🗑️ Clear All", variant="stop", size="sm")

                # Save section
                gr.Markdown("---")
                gr.Markdown("### 💾 Save Your Work")

                with gr.Row():
                    save_path_input = gr.Textbox(
                        label="Save Path",
                        placeholder="output/my_image.png (leave empty for auto-generated name)",
                        value="",
                        scale=3
                    )
                    save_btn = gr.Button("💾 Save Image", variant="primary", size="lg", scale=1)

                save_status = gr.Textbox(
                    label="Save Status",
                    interactive=False,
                    lines=2,
                    value="Enter a path and click 'Save Image' to save your work"
                )

                gr.Markdown("---")

                status_text = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=3,
                    value="Upload an image to get started!"
                )

                overlay_list = gr.Textbox(
                    label="Placed Features",
                    interactive=False,
                    lines=4
                )

            # Right column - Controls
            with gr.Column(scale=1):
                gr.Markdown("### 1. Select Category")
                category_select = gr.Radio(
                    choices=["eyes", "mustache", "eyeglasses", "left_eyebrow", 'right_eyebrow', 'lips',
                             'nose'],  # Add more as needed
                    value="eyes",
                    label="Feature Category"
                )

                gr.Markdown("### 2. Choose Style from Catalog")
                catalog_gallery = gr.Gallery(
                    label="Click to Select",
                    show_label=True,
                    columns=2,
                    rows=3,
                    height="400px",
                    object_fit="contain"
                )

                gr.Markdown("### 3. 👁️ LIVE PREVIEW - Adjust & Watch!")
                gr.Markdown("**The ENTIRE image is always visible - just scaled to different sizes!**")

                feature_preview = gr.Image(
                    label="🔍 Full Feature Preview (entire image visible at all scales)",
                    type="pil",
                    interactive=False,
                    height=400
                )

                scale_slider = gr.Slider(
                    minimum=0.02,
                    maximum=0.5,
                    value=0.1,
                    step=0.01,
                    label="📏 Size (0.01x - 0.5x) - DRAG TO SEE CHANGES!"
                )

                rotation_slider = gr.Slider(
                    minimum=-180,
                    maximum=180,
                    value=0,
                    step=5,
                    label="🔄 Rotation (degrees)"
                )

                opacity_slider = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=1.0,
                    step=0.1,
                    label="👻 Opacity (transparency)"
                )

                gr.Markdown("### 4. Click on Image to Place")
                gr.Markdown("💡 **Tip:** Adjust size first, then click where you want it!")

        # Event handlers

        # Handle image upload (separate from clicks)
        image_display.upload(
            fn=editor.handle_image_upload,
            inputs=[image_display],
            outputs=[image_display, status_text]
        )

        # Update catalog when category changes - now ONLY updates gallery
        category_select.change(
            fn=editor.change_category,
            inputs=[category_select],
            outputs=[image_display, catalog_gallery]
        )

        # Initialize catalog with default category
        interface.load(
            fn=editor.create_catalog_gallery,
            inputs=[category_select],
            outputs=[catalog_gallery]
        )

        # Select from catalog - now with auto-confirm and optimized image updates
        catalog_gallery.select(
            fn=editor.select_from_catalog,
            inputs=[category_select],
            outputs=[image_display, status_text, feature_preview, scale_slider, rotation_slider, opacity_slider]
        )

        # Click on image to place/move feature
        image_display.select(
            fn=editor.handle_image_click,
            inputs=[image_display],
            outputs=[image_display, status_text]
        )

        # Confirm placement button
        confirm_btn.click(
            fn=editor.confirm_placement,
            outputs=[image_display, status_text]
        )

        # Cancel preview button
        cancel_btn.click(
            fn=editor.cancel_preview,
            outputs=[image_display, status_text]
        )

        # Control buttons
        undo_btn.click(
            fn=editor.undo_last,
            outputs=[image_display, status_text]
        )

        clear_btn.click(
            fn=editor.clear_all,
            outputs=[image_display, status_text]
        )

        # Save button
        save_btn.click(
            fn=editor.save_image,
            inputs=[save_path_input],
            outputs=[save_status]
        )

        # Update settings - THESE UPDATE THE PREVIEW IN REAL-TIME!
        scale_slider.change(
            fn=editor.update_scale,
            inputs=[scale_slider],
            outputs=[image_display, status_text, feature_preview]
        )

        rotation_slider.change(
            fn=editor.update_rotation,
            inputs=[rotation_slider],
            outputs=[image_display, status_text, feature_preview]
        )

        opacity_slider.change(
            fn=editor.update_opacity,
            inputs=[opacity_slider],
            outputs=[image_display, status_text, feature_preview]
        )

        # Update overlay list when image changes
        image_display.change(
            fn=editor.get_overlay_list,
            outputs=[overlay_list]
        )

    return interface


if __name__ == "__main__":
    app = create_interface()
    app.launch(share=False, server_port=7861)