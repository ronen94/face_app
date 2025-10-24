import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from typing import Optional, Tuple, List
import base64
from io import BytesIO


class InteractiveFacialEditor:
    def __init__(self):
        self.base_image = None
        self.overlays = []
        self.selected_feature = "sunglasses"
        self.current_scale = 1.0
        self.current_rotation = 0
        self.current_opacity = 1.0
        self.feature_assets = {}
        self.custom_features = {}
        self.init_default_features()
        self.preview_mode = False

    def init_default_features(self):
        """Initialize with default drawn features - same as before"""
        features = {}

        # Sunglasses with reflection effect
        sunglasses = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses)
        # Lenses
        draw.ellipse([20, 15, 85, 65], fill=(20, 20, 20, 200), outline=(60, 60, 60, 255), width=3)
        draw.ellipse([115, 15, 180, 65], fill=(20, 20, 20, 200), outline=(60, 60, 60, 255), width=3)
        # Reflection on lenses
        draw.ellipse([30, 25, 45, 35], fill=(100, 100, 150, 100))
        draw.ellipse([125, 25, 140, 35], fill=(100, 100, 150, 100))
        # Bridge and arms
        draw.rectangle([83, 38, 117, 42], fill=(60, 60, 60, 255))
        draw.rectangle([15, 38, 25, 42], fill=(60, 60, 60, 255))
        draw.rectangle([175, 38, 185, 42], fill=(60, 60, 60, 255))
        features['sunglasses'] = sunglasses

        # Realistic Beard
        beard = Image.new('RGBA', (180, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard)
        # Base shape
        draw.ellipse([30, 20, 150, 120], fill=(45, 28, 18, 180))
        # Add texture and depth
        for _ in range(30):
            x = np.random.randint(35, 145)
            y = np.random.randint(25, 115)
            w = np.random.randint(2, 5)
            h = np.random.randint(5, 12)
            draw.ellipse([x, y, x + w, y + h], fill=(35, 20, 12, 120))
        features['beard'] = beard

        # Handlebar Mustache
        mustache = Image.new('RGBA', (160, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache)
        # Curved mustache shape
        draw.chord([20, 20, 70, 40], 0, 180, fill=(45, 28, 18, 200))
        draw.chord([90, 20, 140, 40], 0, 180, fill=(45, 28, 18, 200))
        draw.rectangle([68, 25, 92, 35], fill=(45, 28, 18, 200))
        # Add curled ends
        draw.arc([10, 25, 30, 35], 90, 270, fill=(45, 28, 18, 200), width=3)
        draw.arc([130, 25, 150, 35], 270, 90, fill=(45, 28, 18, 200), width=3)
        features['mustache'] = mustache

        # Fancy Top Hat
        hat = Image.new('RGBA', (200, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat)
        # Shadow
        draw.ellipse([15, 105, 195, 145], fill=(0, 0, 0, 50))
        # Brim
        draw.ellipse([10, 100, 190, 140], fill=(30, 30, 30, 220), outline=(20, 20, 20, 255), width=2)
        # Crown
        draw.rectangle([50, 30, 150, 110], fill=(35, 35, 35, 220))
        # Hat band
        draw.rectangle([50, 85, 150, 100], fill=(180, 30, 30, 220))
        # Highlight
        draw.rectangle([55, 35, 145, 45], fill=(50, 50, 50, 150))
        features['tophat'] = hat

        # Wavy Hair
        hair = Image.new('RGBA', (220, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair)
        # Base hair shape
        draw.ellipse([20, 40, 200, 160], fill=(60, 40, 25, 170))
        draw.ellipse([30, 20, 190, 120], fill=(65, 45, 30, 180))
        # Add waves and highlights
        for _ in range(40):
            x = np.random.randint(30, 180)
            y = np.random.randint(25, 140)
            draw.arc([x, y, x + 25, y + 35], 0, 180, fill=(70, 50, 35, 100), width=2)
        features['hair'] = hair

        # Reading Glasses
        glasses = Image.new('RGBA', (180, 70), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glasses)
        # Frames
        draw.rectangle([20, 15, 75, 55], fill=None, outline=(100, 100, 100, 230), width=3)
        draw.rectangle([105, 15, 160, 55], fill=None, outline=(100, 100, 100, 230), width=3)
        # Glass effect
        draw.rectangle([23, 18, 72, 52], fill=(200, 200, 255, 30))
        draw.rectangle([108, 18, 157, 52], fill=(200, 200, 255, 30))
        # Bridge and arms
        draw.line([75, 35, 105, 35], fill=(100, 100, 100, 230), width=2)
        draw.line([20, 35, 10, 35], fill=(100, 100, 100, 230), width=2)
        draw.line([160, 35, 170, 35], fill=(100, 100, 100, 230), width=2)
        features['glasses'] = glasses

        # Fancy Bow Tie
        bowtie = Image.new('RGBA', (120, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bowtie)
        # Wings with gradient effect
        draw.polygon([(60, 30), (20, 15), (20, 45), (60, 30)],
                     fill=(150, 30, 30, 220), outline=(100, 20, 20, 255), width=2)
        draw.polygon([(60, 30), (100, 15), (100, 45), (60, 30)],
                     fill=(150, 30, 30, 220), outline=(100, 20, 20, 255), width=2)
        # Center knot
        draw.ellipse([50, 25, 70, 35], fill=(100, 20, 20, 240))
        # Pattern
        for i in range(3):
            draw.line([25 + i * 10, 20, 25 + i * 10, 40], fill=(180, 60, 60, 150), width=1)
            draw.line([85 + i * 10, 20, 85 + i * 10, 40], fill=(180, 60, 60, 150), width=1)
        features['bowtie'] = bowtie

        # Gold Earrings
        earrings = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(earrings)
        # Left earring - hoop with charm
        draw.ellipse([20, 30, 45, 55], fill=None, outline=(255, 215, 0, 255), width=4)
        draw.ellipse([27, 52, 38, 63], fill=(255, 215, 0, 255))
        draw.ellipse([29, 54, 36, 61], fill=(255, 235, 100, 200))  # Highlight
        # Right earring
        draw.ellipse([155, 30, 180, 55], fill=None, outline=(255, 215, 0, 255), width=4)
        draw.ellipse([162, 52, 173, 63], fill=(255, 215, 0, 255))
        draw.ellipse([164, 54, 171, 61], fill=(255, 235, 100, 200))  # Highlight
        features['earrings'] = earrings

        # Red Clown Nose
        nose = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(nose)
        # Shadow
        draw.ellipse([12, 12, 52, 52], fill=(150, 0, 0, 100))
        # Main nose
        draw.ellipse([10, 10, 50, 50], fill=(255, 0, 0, 220))
        # Highlights
        draw.ellipse([18, 16, 28, 26], fill=(255, 100, 100, 200))
        draw.ellipse([22, 20, 26, 24], fill=(255, 200, 200, 255))
        features['clown_nose'] = nose

        # Pirate Eye Patch
        eyepatch = Image.new('RGBA', (100, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(eyepatch)
        # Patch
        draw.ellipse([25, 20, 75, 60], fill=(20, 20, 20, 230), outline=(10, 10, 10, 255), width=3)
        # Strap
        draw.line([25, 40, 5, 35], fill=(20, 20, 20, 230), width=4)
        draw.line([75, 40, 95, 35], fill=(20, 20, 20, 230), width=4)
        # Skull decoration
        draw.ellipse([45, 35, 55, 45], fill=(200, 200, 200, 200))
        features['eyepatch'] = eyepatch

        # Monocle
        monocle = Image.new('RGBA', (80, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(monocle)
        # Glass
        draw.ellipse([15, 15, 65, 65], fill=(200, 200, 255, 40), outline=(150, 120, 50, 230), width=3)
        # Chain
        draw.line([40, 65, 40, 95], fill=(150, 120, 50, 230), width=2)
        draw.ellipse([35, 90, 45, 100], fill=None, outline=(150, 120, 50, 230), width=2)
        # Reflection
        draw.arc([20, 20, 40, 40], 180, 270, fill=(255, 255, 255, 100), width=2)
        features['monocle'] = monocle

        # Baseball Cap
        cap = Image.new('RGBA', (180, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(cap)
        # Crown
        draw.ellipse([40, 30, 140, 80], fill=(50, 100, 200, 220))
        # Visor
        draw.ellipse([30, 50, 150, 90], fill=(40, 80, 160, 230))
        draw.chord([30, 50, 150, 90], 0, 180, fill=(30, 60, 120, 240))
        # Button on top
        draw.ellipse([85, 35, 95, 45], fill=(60, 120, 240, 255))
        features['cap'] = cap

        # Crown
        crown = Image.new('RGBA', (200, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(crown)
        # Base
        draw.rectangle([30, 60, 170, 100], fill=(255, 215, 0, 230), outline=(200, 170, 0, 255), width=2)
        # Peaks
        peaks = [(30, 60), (50, 30), (70, 60), (90, 30), (110, 60), (130, 30), (150, 60), (170, 30), (170, 60)]
        draw.polygon(peaks, fill=(255, 215, 0, 230), outline=(200, 170, 0, 255), width=2)
        # Jewels
        draw.ellipse([85, 70, 115, 90], fill=(255, 0, 100, 200), outline=(200, 0, 80, 255))
        draw.ellipse([45, 75, 60, 85], fill=(0, 100, 255, 200), outline=(0, 80, 200, 255))
        draw.ellipse([140, 75, 155, 85], fill=(0, 255, 100, 200), outline=(0, 200, 80, 255))
        features['crown'] = crown

        self.feature_assets = features

    def process_click(self, image, evt: gr.SelectData):
        """Handle click on image to place feature"""
        if image is None:
            return None, "⚠️ Please upload an image first!", self.get_overlay_list()

        # Initialize base image if needed
        if self.base_image is None:
            self.base_image = Image.fromarray(image).convert('RGBA')

        # Get normalized coordinates
        height, width = image.shape[:2]
        x_norm = evt.index[0] / width
        y_norm = evt.index[1] / height

        # Add the feature
        self.add_feature_at(x_norm, y_norm)

        return (
            self.render_image(),
            f"✅ Placed {self.selected_feature} at ({x_norm:.2f}, {y_norm:.2f})",
            self.get_overlay_list()
        )

    def add_feature_at(self, x, y):
        """Add feature at specific normalized coordinates"""
        overlay = {
            'type': self.selected_feature,
            'x': x,
            'y': y,
            'scale': self.current_scale,
            'rotation': self.current_rotation,
            'opacity': self.current_opacity
        }
        self.overlays.append(overlay)

    def update_settings(self, feature, scale, rotation, opacity):
        """Update current settings"""
        self.selected_feature = feature if feature else "sunglasses"
        self.current_scale = scale
        self.current_rotation = rotation
        self.current_opacity = opacity
        return f"✏️ Ready to place: {self.selected_feature}"

    def quick_select_feature(self, feature_name):
        """Quick select a feature"""
        self.selected_feature = feature_name
        return feature_name, f"✏️ Selected: {feature_name}"

    def undo_last(self):
        """Remove the last added feature"""
        if self.overlays:
            removed = self.overlays.pop()
            return (
                self.render_image(),
                f"↩️ Removed {removed['type']}",
                self.get_overlay_list()
            )
        return self.render_image(), "Nothing to undo", self.get_overlay_list()

    def clear_all(self):
        """Clear all overlays"""
        count = len(self.overlays)
        self.overlays = []
        return (
            self.render_image(),
            f"🗑️ Cleared {count} features",
            self.get_overlay_list()
        )

    def get_overlay_list(self):
        """Get formatted list of overlays"""
        if not self.overlays:
            return "📝 No features added yet\n\nClick on the image to place features!"

        text = f"📊 Total Features: {len(self.overlays)}\n"
        text += "─" * 45 + "\n"

        for i, overlay in enumerate(self.overlays):
            text += f" {i:2d} │ {overlay['type']:12} │ "
            text += f"Pos: ({overlay['x']:.2f},{overlay['y']:.2f}) │ "
            text += f"Size: {overlay['scale']:.1f}×\n"

        return text

    def render_image(self):
        """Render the final image with all overlays"""
        if self.base_image is None:
            # Create instruction placeholder
            placeholder = Image.new('RGBA', (600, 400), (230, 230, 230, 255))
            draw = ImageDraw.Draw(placeholder)

            # Draw upload icon (simplified cloud with arrow)
            draw.ellipse([270, 150, 330, 180], fill=(150, 150, 150, 255))
            draw.polygon([(290, 180), (310, 180), (300, 195)], fill=(150, 150, 150, 255))

            # Instructions
            draw.text((200, 220), "Click here to upload an image", fill=(100, 100, 100, 255))
            draw.text((180, 250), "Then click anywhere to place features!", fill=(120, 120, 120, 255))

            return np.array(placeholder)

        # Render with overlays
        result = self.base_image.copy()

        for overlay in self.overlays:
            feature = self.feature_assets.get(overlay['type'])
            if not feature:
                continue

            # Transform feature
            transformed = feature.copy()

            # Scale
            new_size = (
                int(feature.width * overlay['scale']),
                int(feature.height * overlay['scale'])
            )
            transformed = transformed.resize(new_size, Image.Resampling.LANCZOS)

            # Rotation
            if overlay['rotation'] != 0:
                transformed = transformed.rotate(
                    -overlay['rotation'],
                    expand=True,
                    fillcolor=(0, 0, 0, 0)
                )

            # Opacity
            if overlay['opacity'] < 1.0:
                alpha = transformed.split()[3]
                alpha = alpha.point(lambda p: int(p * overlay['opacity']))
                transformed.putalpha(alpha)

            # Position (centered at click point)
            x = int(overlay['x'] * result.width - transformed.width // 2)
            y = int(overlay['y'] * result.height - transformed.height // 2)

            # Paste onto result
            result.paste(transformed, (x, y), transformed)

        return np.array(result)

    def save_image(self):
        """Save the final image"""
        if self.base_image is None:
            return None, "❌ No image to save!"

        result = Image.fromarray(self.render_image())
        output_path = "/home/claude/facial_edit_final.png"
        result.save(output_path)
        return output_path, f"✅ Saved! ({len(self.overlays)} features)"

    def load_custom_feature(self, name, image):
        """Load a custom feature"""
        if image is not None and name:
            custom_img = Image.fromarray(image).convert('RGBA')
            # Resize if too large
            if custom_img.width > 300 or custom_img.height > 300:
                custom_img.thumbnail((300, 300), Image.Resampling.LANCZOS)

            feature_key = f"custom_{name}"
            self.feature_assets[feature_key] = custom_img

            # Return updated choices
            return (
                f"✅ Added custom: {name}",
                gr.update(choices=list(self.feature_assets.keys()), value=feature_key)
            )
        return "❌ Need both name and image", gr.update()


def create_interface():
    editor = InteractiveFacialEditor()

    # Custom CSS for better styling
    custom_css = """
    .quick-btn {
        min-height: 50px;
        font-size: 24px;
        border-radius: 10px;
    }
    .main-image {
        border: 2px dashed #ccc;
        border-radius: 10px;
        cursor: crosshair;
    }
    .overlay-list {
        font-family: 'Courier New', monospace;
        background: #f5f5f5;
        border-radius: 5px;
        padding: 10px;
    }
    """

    with gr.Blocks(
            title="Click-to-Place Facial Editor",
            theme=gr.themes.Soft(),
            css=custom_css
    ) as interface:
        # Header
        gr.Markdown("""
        # 🎯 Interactive Facial Feature Editor
        ### Simply click on your photo to add fun features! No dragging needed!
        """)

        with gr.Row():
            # Main image area
            with gr.Column(scale=3):
                main_image = gr.Image(
                    label="📸 Your Canvas (Click to Place Features)",
                    type="numpy",
                    interactive=True,
                    elem_classes="main-image",
                    height=500
                )

                # Action buttons
                with gr.Row():
                    save_btn = gr.Button("💾 Save", variant="primary", size="lg")
                    undo_btn = gr.Button("↩️ Undo", variant="secondary", size="lg")
                    clear_btn = gr.Button("🗑️ Clear", variant="stop", size="lg")

                status_text = gr.Textbox(
                    label="Status",
                    value="👆 Upload an image to start!",
                    interactive=False
                )

            # Controls panel
            with gr.Column(scale=1):
                gr.Markdown("## 🎨 Feature Palette")

                # Quick access buttons
                gr.Markdown("**Quick Select** (click then click image):")
                with gr.Row():
                    btn_sunglasses = gr.Button("🕶️", elem_classes="quick-btn", size="sm")
                    btn_mustache = gr.Button("👨", elem_classes="quick-btn", size="sm")
                    btn_hat = gr.Button("🎩", elem_classes="quick-btn", size="sm")
                    btn_crown = gr.Button("👑", elem_classes="quick-btn", size="sm")

                with gr.Row():
                    btn_beard = gr.Button("🧔", elem_classes="quick-btn", size="sm")
                    btn_glasses = gr.Button("👓", elem_classes="quick-btn", size="sm")
                    btn_nose = gr.Button("🔴", elem_classes="quick-btn", size="sm")
                    btn_cap = gr.Button("🧢", elem_classes="quick-btn", size="sm")

                # Full selection dropdown
                feature_select = gr.Dropdown(
                    choices=list(editor.feature_assets.keys()),
                    value="sunglasses",
                    label="All Features:",
                    interactive=True
                )

                # Transform controls
                gr.Markdown("### ⚙️ Adjust Settings")
                scale_control = gr.Slider(
                    minimum=0.3, maximum=2.5, value=1.0, step=0.1,
                    label="Size", info="Make it bigger or smaller"
                )

                rotation_control = gr.Slider(
                    minimum=-180, maximum=180, value=0, step=5,
                    label="Rotation", info="Tilt left or right"
                )

                opacity_control = gr.Slider(
                    minimum=0.2, maximum=1.0, value=1.0, step=0.1,
                    label="Opacity", info="Make it transparent"
                )

                # Custom feature upload
                with gr.Accordion("📤 Custom Features", open=False):
                    custom_name_input = gr.Textbox(
                        label="Name your feature:",
                        placeholder="e.g., funny_hat"
                    )
                    custom_img_input = gr.Image(
                        label="Upload PNG with transparency:",
                        type="numpy",
                        height=120
                    )
                    custom_add_btn = gr.Button("Add Custom Feature", variant="secondary")

                # Overlay list
                gr.Markdown("### 📋 Placed Features")
                overlay_display = gr.Textbox(
                    label="",
                    value=editor.get_overlay_list(),
                    lines=7,
                    interactive=False,
                    elem_classes="overlay-list"
                )

        # Tips section
        with gr.Accordion("💡 Pro Tips", open=False):
            gr.Markdown("""
            - **Click precisely** where you want the center of the feature
            - **Adjust settings first** before clicking to place
            - **Layer order** matters - features stack in order added
            - **Use opacity** for subtle, blended effects
            - **Rotation** helps match head angles
            - **Custom features** work best as PNG with transparency
            - **Keyboard shortcuts**: Coming soon!
            """)

        # Wire up all the interactions

        # Main image click handler
        main_image.select(
            fn=editor.process_click,
            inputs=[main_image],
            outputs=[main_image, status_text, overlay_display]
        )

        # Settings updates
        for control in [feature_select, scale_control, rotation_control, opacity_control]:
            control.change(
                fn=editor.update_settings,
                inputs=[feature_select, scale_control, rotation_control, opacity_control],
                outputs=[status_text]
            )

        # Quick select buttons
        btn_sunglasses.click(
            fn=lambda: editor.quick_select_feature("sunglasses"),
            outputs=[feature_select, status_text]
        )
        btn_mustache.click(
            fn=lambda: editor.quick_select_feature("mustache"),
            outputs=[feature_select, status_text]
        )
        btn_hat.click(
            fn=lambda: editor.quick_select_feature("tophat"),
            outputs=[feature_select, status_text]
        )
        btn_crown.click(
            fn=lambda: editor.quick_select_feature("crown"),
            outputs=[feature_select, status_text]
        )
        btn_beard.click(
            fn=lambda: editor.quick_select_feature("beard"),
            outputs=[feature_select, status_text]
        )
        btn_glasses.click(
            fn=lambda: editor.quick_select_feature("glasses"),
            outputs=[feature_select, status_text]
        )
        btn_nose.click(
            fn=lambda: editor.quick_select_feature("clown_nose"),
            outputs=[feature_select, status_text]
        )
        btn_cap.click(
            fn=lambda: editor.quick_select_feature("cap"),
            outputs=[feature_select, status_text]
        )

        # Action buttons
        undo_btn.click(
            fn=editor.undo_last,
            outputs=[main_image, status_text, overlay_display]
        )

        clear_btn.click(
            fn=editor.clear_all,
            outputs=[main_image, status_text, overlay_display]
        )

        save_btn.click(
            fn=editor.save_image,
            outputs=[gr.File(label="Download your creation!"), status_text]
        )

        # Custom feature loading
        custom_add_btn.click(
            fn=editor.load_custom_feature,
            inputs=[custom_name_input, custom_img_input],
            outputs=[status_text, feature_select]
        )

    return interface


if __name__ == "__main__":
    app = create_interface()
    app.launch(share=True, debug=True)