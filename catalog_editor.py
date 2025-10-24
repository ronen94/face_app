import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path

WORKDIR = Path(__file__).parent

class CatalogEditor:
    def __init__(self):
        self.base_image = None
        self.overlays = []
        self.selected_feature = None
        self.selected_category = "beard"
        self.current_scale = 1.0
        self.current_rotation = 0
        self.current_opacity = 1.0
        self.feature_catalog = {}
        self.preview_overlay = None  # For showing preview before confirming
        self.init_feature_catalog()

    def init_feature_catalog(self):
        """Initialize catalog with multiple variations for each feature type"""

        # BEARD VARIATIONS
        self.feature_catalog['beard'] = {}

        # Full Beard
        beard1 = Image.new('RGBA', (180, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard1)
        draw.ellipse([30, 20, 150, 120], fill=(45, 28, 18, 220))
        draw.ellipse([40, 10, 140, 100], fill=(55, 35, 22, 200))
        self.feature_catalog['beard']['Full Beard'] = beard1

        # Goatee
        beard2 = Image.new('RGBA', (120, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard2)
        draw.ellipse([30, 30, 90, 90], fill=(45, 28, 18, 220))
        draw.rectangle([45, 10, 75, 50], fill=(45, 28, 18, 220))
        self.feature_catalog['beard']['Goatee'] = beard2

        # Short Stubble
        beard3 = Image.new('RGBA', (160, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard3)
        draw.ellipse([30, 20, 130, 100], fill=(60, 40, 30, 150))
        self.feature_catalog['beard']['Stubble'] = beard3

        # Van Dyke
        beard4 = Image.new('RGBA', (140, 110), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard4)
        draw.ellipse([40, 50, 100, 105], fill=(45, 28, 18, 220))
        draw.rectangle([60, 10, 80, 60], fill=(45, 28, 18, 220))
        self.feature_catalog['beard']['Van Dyke'] = beard4

        # Chin Strap
        beard5 = Image.new('RGBA', (180, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard5)
        draw.arc([20, 20, 80, 90], 180, 360, fill=(45, 28, 18, 255), width=15)
        draw.arc([100, 20, 160, 90], 180, 360, fill=(45, 28, 18, 255), width=15)
        draw.line([40, 90, 140, 90], fill=(45, 28, 18, 255), width=15)
        self.feature_catalog['beard']['Chin Strap'] = beard5

        # MUSTACHE VARIATIONS
        self.feature_catalog['mustache'] = {}

        # Handlebar Mustache
        mustache1 = Image.new('RGBA', (180, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache1)
        draw.arc([10, 15, 70, 55], 200, 340, fill=(45, 28, 18, 255), width=12)
        draw.arc([110, 15, 170, 55], 200, 340, fill=(45, 28, 18, 255), width=12)
        draw.rectangle([65, 30, 115, 42], fill=(45, 28, 18, 255))
        self.feature_catalog['mustache']['Handlebar'] = mustache1

        # Pencil Mustache
        mustache2 = Image.new('RGBA', (120, 30), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache2)
        draw.rectangle([20, 12, 100, 18], fill=(45, 28, 18, 255))
        self.feature_catalog['mustache']['Pencil'] = mustache2

        # Walrus Mustache
        mustache3 = Image.new('RGBA', (160, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache3)
        draw.ellipse([20, 10, 70, 70], fill=(45, 28, 18, 220))
        draw.ellipse([90, 10, 140, 70], fill=(45, 28, 18, 220))
        draw.rectangle([60, 30, 100, 50], fill=(45, 28, 18, 220))
        self.feature_catalog['mustache']['Walrus'] = mustache3

        # Chevron Mustache
        mustache4 = Image.new('RGBA', (140, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache4)
        draw.rectangle([20, 15, 120, 35], fill=(45, 28, 18, 240))
        self.feature_catalog['mustache']['Chevron'] = mustache4

        # SUNGLASSES VARIATIONS
        self.feature_catalog['sunglasses'] = {}

        # Aviator
        sunglasses1 = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses1)
        draw.ellipse([20, 15, 85, 65], fill=(20, 20, 20, 180), outline=(50, 50, 50, 255), width=2)
        draw.ellipse([115, 15, 180, 65], fill=(20, 20, 20, 180), outline=(50, 50, 50, 255), width=2)
        draw.rectangle([83, 38, 117, 42], fill=(50, 50, 50, 255))
        self.feature_catalog['sunglasses']['Aviator'] = sunglasses1

        # Wayfarer
        sunglasses2 = Image.new('RGBA', (200, 70), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses2)
        draw.rectangle([20, 15, 85, 55], fill=(20, 20, 20, 200), outline=(10, 10, 10, 255), width=3)
        draw.rectangle([115, 15, 180, 55], fill=(20, 20, 20, 200), outline=(10, 10, 10, 255), width=3)
        draw.rectangle([83, 33, 117, 37], fill=(10, 10, 10, 255))
        self.feature_catalog['sunglasses']['Wayfarer'] = sunglasses2

        # Round Glasses
        sunglasses3 = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses3)
        draw.ellipse([25, 20, 80, 60], fill=(100, 100, 150, 120), outline=(40, 40, 40, 255), width=3)
        draw.ellipse([120, 20, 175, 60], fill=(100, 100, 150, 120), outline=(40, 40, 40, 255), width=3)
        draw.rectangle([78, 38, 122, 42], fill=(40, 40, 40, 255))
        self.feature_catalog['sunglasses']['Round'] = sunglasses3

        # Cat Eye
        sunglasses4 = Image.new('RGBA', (220, 75), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses4)
        pts1 = [(15, 40), (30, 25), (75, 25), (90, 40), (75, 50), (30, 50)]
        draw.polygon(pts1, fill=(20, 20, 20, 200), outline=(10, 10, 10, 255))
        pts2 = [(130, 40), (145, 25), (190, 25), (205, 40), (190, 50), (145, 50)]
        draw.polygon(pts2, fill=(20, 20, 20, 200), outline=(10, 10, 10, 255))
        draw.rectangle([88, 38, 132, 42], fill=(10, 10, 10, 255))
        self.feature_catalog['sunglasses']['Cat Eye'] = sunglasses4

        # HAT VARIATIONS
        self.feature_catalog['hat'] = {}

        # Top Hat
        hat1 = Image.new('RGBA', (160, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat1)
        draw.rectangle([40, 20, 120, 120], fill=(30, 30, 35, 255))
        draw.ellipse([20, 110, 140, 145], fill=(35, 35, 40, 255))
        draw.rectangle([35, 116, 125, 125], fill=(80, 20, 20, 255))
        self.feature_catalog['hat']['Top Hat'] = hat1

        # Baseball Cap
        hat2 = Image.new('RGBA', (180, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat2)
        draw.ellipse([30, 30, 150, 85], fill=(200, 50, 50, 255))
        draw.ellipse([20, 55, 90, 95], fill=(180, 40, 40, 255))
        self.feature_catalog['hat']['Baseball Cap'] = hat2

        # Cowboy Hat
        hat3 = Image.new('RGBA', (200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat3)
        draw.ellipse([20, 70, 180, 110], fill=(139, 90, 43, 255))
        pts = [(100, 25), (60, 70), (140, 70)]
        draw.polygon(pts, fill=(160, 100, 50, 255))
        draw.ellipse([70, 60, 130, 85], fill=(139, 90, 43, 255))
        self.feature_catalog['hat']['Cowboy'] = hat3

        # Beanie
        hat4 = Image.new('RGBA', (140, 90), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat4)
        draw.ellipse([20, 30, 120, 80], fill=(100, 100, 120, 255))
        draw.ellipse([50, 15, 90, 45], fill=(100, 100, 120, 255))
        self.feature_catalog['hat']['Beanie'] = hat4

        # HAIR VARIATIONS
        self.feature_catalog['hair'] = {}

        # Afro
        hair1 = Image.new('RGBA', (200, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair1)
        draw.ellipse([20, 20, 180, 160], fill=(45, 28, 18, 255))
        self.feature_catalog['hair']['Afro'] = hair1

        # Long Hair
        hair2 = Image.new('RGBA', (220, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair2)
        draw.ellipse([30, 10, 100, 80], fill=(60, 40, 20, 255))
        draw.ellipse([120, 10, 190, 80], fill=(60, 40, 20, 255))
        draw.rectangle([30, 50, 190, 180], fill=(60, 40, 20, 255))
        self.feature_catalog['hair']['Long Hair'] = hair2

        # Mohawk
        hair3 = Image.new('RGBA', (80, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair3)
        draw.rectangle([25, 20, 55, 140], fill=(200, 50, 50, 255))
        draw.polygon([(25, 20), (40, 5), (55, 20)], fill=(200, 50, 50, 255))
        self.feature_catalog['hair']['Mohawk'] = hair3

        # Bob Cut
        hair4 = Image.new('RGBA', (180, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair4)
        draw.ellipse([20, 10, 160, 90], fill=(139, 69, 19, 255))
        draw.rectangle([20, 50, 160, 120], fill=(139, 69, 19, 255))
        self.feature_catalog['hair']['Bob Cut'] = hair4

        # EYEWEAR VARIATIONS
        self.feature_catalog['glasses'] = {}

        # Nerd Glasses
        glasses1 = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glasses1)
        draw.rectangle([20, 25, 80, 60], fill=(255, 255, 255, 100), outline=(20, 20, 20, 255), width=4)
        draw.rectangle([120, 25, 180, 60], fill=(255, 255, 255, 100), outline=(20, 20, 20, 255), width=4)
        draw.rectangle([78, 40, 122, 45], fill=(20, 20, 20, 255))
        self.feature_catalog['glasses']['Nerd Glasses'] = glasses1

        # Reading Glasses
        glasses2 = Image.new('RGBA', (180, 70), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glasses2)
        draw.ellipse([20, 20, 75, 60], fill=(255, 255, 255, 80), outline=(100, 80, 60, 255), width=2)
        draw.ellipse([105, 20, 160, 60], fill=(255, 255, 255, 80), outline=(100, 80, 60, 255), width=2)
        draw.rectangle([73, 38, 107, 42], fill=(100, 80, 60, 255))
        self.feature_catalog['glasses']['Reading'] = glasses2

        # Monocle
        glasses3 = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glasses3)
        draw.ellipse([20, 20, 80, 80], fill=(255, 255, 255, 100), outline=(180, 150, 100, 255), width=3)
        draw.rectangle([75, 48, 90, 52], fill=(180, 150, 100, 255))
        self.feature_catalog['glasses']['Monocle'] = glasses3

        self.feature_catalog['eyes'] = {}
        self.feature_catalog['eyes']['Blue Eyes'] = Image.open(os.path.join(WORKDIR, 'assets', 'eye_images', 'blue_eye1.png')).convert('RGBA').resize((80, 50), Image.Resampling.LANCZOS)

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

    def select_from_catalog(self, evt: gr.SelectData, category):
        """Handle selection from the catalog gallery"""
        selected_name = evt.value['caption']
        self.selected_feature = (category, selected_name)
        return f"✓ Selected: {selected_name} from {category}"

    def handle_image_click(self, img, evt: gr.SelectData):
        """Place or move the selected feature where the user clicked"""
        if img is None:
            return None, "❌ Please upload an image first"

        # Set base image if this is first interaction
        if self.base_image is None:
            self.base_image = Image.fromarray(img).convert('RGBA')
            return self.base_image, "✓ Image loaded! Select a feature from the catalog."

        if self.selected_feature is None:
            return self.composite_image(), "❌ Please select a feature from the catalog first"

        category, feature_name = self.selected_feature
        feature_img = self.feature_catalog[category][feature_name].copy()

        # Get click coordinates - evt.index contains (x, y) pixel coordinates
        click_x = evt.index[0]
        click_y = evt.index[1]

        # Apply transformations
        if self.current_scale != 1.0:
            new_size = (int(feature_img.width * self.current_scale),
                        int(feature_img.height * self.current_scale))
            feature_img = feature_img.resize(new_size, Image.Resampling.LANCZOS)

        if self.current_rotation != 0:
            feature_img = feature_img.rotate(self.current_rotation, expand=True,
                                             resample=Image.Resampling.BICUBIC)

        if self.current_opacity != 1.0:
            feature_array = np.array(feature_img)
            feature_array[:, :, 3] = (feature_array[:, :, 3] * self.current_opacity).astype(np.uint8)
            feature_img = Image.fromarray(feature_array)

        # If we have a preview overlay, we're moving it
        if self.preview_overlay is not None:
            # Update the preview position
            self.preview_overlay['x'] = click_x
            self.preview_overlay['y'] = click_y
            result = self.composite_image()
            return result, f"🔄 Moved {feature_name} to ({click_x}, {click_y}). Click 'Confirm' or click again to adjust."
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
            return result, f"✓ Preview: {feature_name} at ({click_x}, {click_y}). Click 'Confirm' to keep it, or click again to move it."

    def confirm_placement(self):
        """Confirm the current preview and add it to overlays"""
        if self.preview_overlay is None:
            return self.composite_image(), "❌ No feature to confirm"

        self.overlays.append(self.preview_overlay)
        feature_name = self.preview_overlay['name']
        self.preview_overlay = None
        result = self.composite_image()
        return result, f"✅ Confirmed {feature_name}! Select another feature or adjust this one."

    def cancel_preview(self):
        """Cancel the current preview"""
        if self.preview_overlay is None:
            return self.composite_image(), "❌ No preview to cancel"

        self.preview_overlay = None
        result = self.composite_image()
        return result, "↩️ Preview cancelled"

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
            # If there's a preview, cancel it first
            self.preview_overlay = None
            result = self.composite_image()
            return result, "↩️ Cancelled preview"

        if not self.overlays:
            return self.composite_image(), "❌ Nothing to undo"

        self.overlays.pop()
        result = self.composite_image()
        return result, "✓ Undid last action"

    def clear_all(self):
        """Remove all overlays and preview"""
        self.overlays = []
        self.preview_overlay = None
        return self.base_image if self.base_image else None, "✓ Cleared all features"

    def update_scale(self, scale):
        """Update the current scale setting"""
        self.current_scale = scale
        return f"Scale: {scale:.2f}x"

    def update_rotation(self, rotation):
        """Update the current rotation setting"""
        self.current_rotation = rotation
        return f"Rotation: {rotation}°"

    def update_opacity(self, opacity):
        """Update the current opacity setting"""
        self.current_opacity = opacity
        return f"Opacity: {int(opacity * 100)}%"

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


def create_interface():
    editor = CatalogEditor()

    with gr.Blocks(title="Feature Catalog Editor", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🎨 Feature Catalog Editor")
        gr.Markdown("Upload an image, select features from the catalog, and click on the image to place them!")

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

                status_text = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=2,
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
                    choices=["beard", "mustache", "sunglasses", "glasses", "hat", "hair", 'eyes'],
                    value="beard",
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

                gr.Markdown("### 3. Adjust Settings (Optional)")
                scale_slider = gr.Slider(
                    minimum=0.3,
                    maximum=3.0,
                    value=1.0,
                    step=0.1,
                    label="Size"
                )

                rotation_slider = gr.Slider(
                    minimum=-180,
                    maximum=180,
                    value=0,
                    step=5,
                    label="Rotation (degrees)"
                )

                opacity_slider = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=1.0,
                    step=0.1,
                    label="Opacity"
                )

                gr.Markdown("### 4. Click on Image")
                gr.Markdown("Click where you want to place the feature. Click again to move it before confirming.")

        # Event handlers

        # Update catalog when category changes
        category_select.change(
            fn=editor.create_catalog_gallery,
            inputs=[category_select],
            outputs=[catalog_gallery]
        )

        # Initialize catalog with default category
        interface.load(
            fn=editor.create_catalog_gallery,
            inputs=[category_select],
            outputs=[catalog_gallery]
        )

        # Select from catalog
        catalog_gallery.select(
            fn=editor.select_from_catalog,
            inputs=[category_select],
            outputs=[status_text]
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

        # Update settings
        scale_slider.change(
            fn=editor.update_scale,
            inputs=[scale_slider],
            outputs=[]
        )

        rotation_slider.change(
            fn=editor.update_rotation,
            inputs=[rotation_slider],
            outputs=[]
        )

        opacity_slider.change(
            fn=editor.update_opacity,
            inputs=[opacity_slider],
            outputs=[]
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