import gradio as gr
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Dict, Optional, Tuple
import json

class ClickToPlaceEditor:
    def __init__(self):
        self.base_image = None
        self.overlays = []
        self.selected_feature = "sunglasses"
        self.current_scale = 1.0
        self.current_rotation = 0
        self.current_opacity = 1.0
        self.feature_assets = {}
        self.init_default_features()
        self.last_click_pos = (0.5, 0.5)
        
    def init_default_features(self):
        """Initialize with default drawn features"""
        features = {}
        
        # Aviator Sunglasses
        sunglasses = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(sunglasses)
        draw.ellipse([20, 15, 85, 65], fill=(20, 20, 20, 180), outline=(50, 50, 50, 255), width=2)
        draw.ellipse([115, 15, 180, 65], fill=(20, 20, 20, 180), outline=(50, 50, 50, 255), width=2)
        draw.rectangle([83, 38, 117, 42], fill=(50, 50, 50, 255))
        draw.rectangle([15, 38, 25, 42], fill=(50, 50, 50, 255))
        draw.rectangle([175, 38, 185, 42], fill=(50, 50, 50, 255))
        features['sunglasses'] = sunglasses
        
        # Beard
        beard = Image.new('RGBA', (180, 140), (0, 0, 0, 0))
        draw = ImageDraw.Draw(beard)
        draw.ellipse([30, 20, 150, 120], fill=(45, 28, 18, 160))
        for i in range(20):
            x = np.random.randint(40, 140)
            y = np.random.randint(30, 110)
            draw.ellipse([x, y, x+3, y+8], fill=(35, 20, 12, 100))
        features['beard'] = beard
        
        # Mustache
        mustache = Image.new('RGBA', (160, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(mustache)
        draw.chord([20, 20, 70, 40], 0, 180, fill=(45, 28, 18, 180), outline=(35, 20, 12, 200))
        draw.chord([90, 20, 140, 40], 0, 180, fill=(45, 28, 18, 180), outline=(35, 20, 12, 200))
        draw.rectangle([68, 25, 92, 35], fill=(45, 28, 18, 180))
        features['mustache'] = mustache
        
        # Top Hat
        hat = Image.new('RGBA', (200, 150), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hat)
        draw.ellipse([10, 100, 190, 140], fill=(30, 30, 30, 200), outline=(20, 20, 20, 255), width=2)
        draw.rectangle([50, 30, 150, 110], fill=(30, 30, 30, 200), outline=(20, 20, 20, 255), width=2)
        draw.rectangle([50, 90, 150, 100], fill=(150, 30, 30, 200))
        features['tophat'] = hat
        
        # Hair/Wig
        hair = Image.new('RGBA', (220, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(hair)
        draw.ellipse([20, 40, 200, 160], fill=(60, 40, 25, 150))
        draw.ellipse([30, 20, 190, 120], fill=(60, 40, 25, 170))
        for i in range(30):
            x = np.random.randint(30, 190)
            y = np.random.randint(25, 150)
            draw.arc([x, y, x+20, y+30], 0, 180, fill=(50, 30, 20, 100), width=2)
        features['hair'] = hair
        
        # Glasses
        glasses = Image.new('RGBA', (180, 70), (0, 0, 0, 0))
        draw = ImageDraw.Draw(glasses)
        draw.rectangle([20, 15, 75, 55], fill=None, outline=(80, 80, 80, 200), width=3)
        draw.rectangle([105, 15, 160, 55], fill=None, outline=(80, 80, 80, 200), width=3)
        draw.line([75, 35, 105, 35], fill=(80, 80, 80, 200), width=2)
        draw.line([20, 35, 10, 35], fill=(80, 80, 80, 200), width=2)
        draw.line([160, 35, 170, 35], fill=(80, 80, 80, 200), width=2)
        features['glasses'] = glasses
        
        # Bow Tie
        bowtie = Image.new('RGBA', (120, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bowtie)
        draw.polygon([(60, 30), (20, 15), (20, 45), (60, 30)], 
                    fill=(150, 30, 30, 200), outline=(100, 20, 20, 255))
        draw.polygon([(60, 30), (100, 15), (100, 45), (60, 30)], 
                    fill=(150, 30, 30, 200), outline=(100, 20, 20, 255))
        draw.ellipse([50, 25, 70, 35], fill=(100, 20, 20, 200))
        features['bowtie'] = bowtie
        
        # Earrings
        earrings = Image.new('RGBA', (200, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(earrings)
        draw.ellipse([20, 30, 40, 50], fill=None, outline=(255, 215, 0, 255), width=3)
        draw.ellipse([25, 50, 35, 60], fill=(255, 215, 0, 255))
        draw.ellipse([160, 30, 180, 50], fill=None, outline=(255, 215, 0, 255), width=3)
        draw.ellipse([165, 50, 175, 60], fill=(255, 215, 0, 255))
        features['earrings'] = earrings
        
        # Clown Nose
        nose = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
        draw = ImageDraw.Draw(nose)
        draw.ellipse([10, 10, 50, 50], fill=(255, 0, 0, 200), outline=(200, 0, 0, 255), width=2)
        draw.ellipse([20, 18, 30, 28], fill=(255, 100, 100, 150))
        features['clown_nose'] = nose
        
        # Eye Patch
        eyepatch = Image.new('RGBA', (100, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(eyepatch)
        draw.ellipse([25, 20, 75, 60], fill=(20, 20, 20, 200), outline=(10, 10, 10, 255), width=2)
        draw.line([25, 40, 10, 35], fill=(20, 20, 20, 200), width=3)
        draw.line([75, 40, 90, 35], fill=(20, 20, 20, 200), width=3)
        features['eyepatch'] = eyepatch
        
        # Monocle
        monocle = Image.new('RGBA', (80, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(monocle)
        draw.ellipse([15, 15, 65, 65], fill=None, outline=(150, 120, 50, 200), width=3)
        draw.ellipse([20, 20, 60, 60], fill=(200, 200, 255, 30))
        draw.line([40, 65, 40, 95], fill=(150, 120, 50, 200), width=2)
        draw.ellipse([35, 90, 45, 100], fill=None, outline=(150, 120, 50, 200), width=2)
        features['monocle'] = monocle
        
        self.feature_assets = features
    
    def load_image(self, image):
        """Load the base image"""
        if image is not None:
            self.base_image = Image.fromarray(image).convert('RGBA')
            self.overlays = []
            return self.render_image(), "✅ Image loaded! Click anywhere on the image to place features.", self.get_overlay_list()
        return None, "Please upload an image", ""
    
    def handle_image_click(self, image, evt: gr.SelectData):
        """Handle click on image to add feature at that position"""
        if self.base_image is None:
            return self.render_image(), "⚠️ Please load an image first!", self.get_overlay_list()
        
        if image is None:
            return self.render_image(), "⚠️ No image loaded", self.get_overlay_list()
        
        # Get click coordinates (normalized 0-1)
        # SelectData provides index which contains [x, y] coordinates
        x_coord = evt.index[0] / image.shape[1]  # Normalize by width
        y_coord = evt.index[1] / image.shape[0]  # Normalize by height
        
        self.last_click_pos = (x_coord, y_coord)
        
        # Add feature at clicked position
        overlay = {
            'type': self.selected_feature,
            'x': x_coord,
            'y': y_coord,
            'scale': self.current_scale,
            'rotation': self.current_rotation,
            'opacity': self.current_opacity
        }
        self.overlays.append(overlay)
        
        return (
            self.render_image(), 
            f"✅ Added {self.selected_feature} at position ({x_coord:.2f}, {y_coord:.2f})",
            self.get_overlay_list()
        )
    
    def update_settings(self, feature, scale, rotation, opacity):
        """Update current settings for new features"""
        self.selected_feature = feature
        self.current_scale = scale
        self.current_rotation = rotation
        self.current_opacity = opacity
        return f"📝 Settings updated: {feature} (scale: {scale:.1f}, rotation: {rotation}°, opacity: {opacity:.1f})"
    
    def preview_at_position(self, x, y):
        """Preview feature at specific position"""
        if self.base_image is None:
            return None
        
        # Temporarily add overlay for preview
        temp_overlay = {
            'type': self.selected_feature,
            'x': x,
            'y': y,
            'scale': self.current_scale,
            'rotation': self.current_rotation,
            'opacity': self.current_opacity * 0.5  # Semi-transparent for preview
        }
        
        self.overlays.append(temp_overlay)
        preview = self.render_image()
        self.overlays.pop()  # Remove preview overlay
        
        return preview
    
    def remove_last_feature(self):
        """Remove the last added feature"""
        if self.overlays:
            removed = self.overlays.pop()
            return self.render_image(), f"❌ Removed {removed['type']}", self.get_overlay_list()
        return self.render_image(), "No features to remove", self.get_overlay_list()
    
    def remove_overlay_by_index(self, index):
        """Remove a specific overlay by index"""
        if 0 <= index < len(self.overlays):
            removed = self.overlays.pop(index)
            return self.render_image(), f"❌ Removed {removed['type']} at index {index}", self.get_overlay_list()
        return self.render_image(), "Invalid overlay index", self.get_overlay_list()
    
    def get_overlay_list(self):
        """Get a formatted list of current overlays"""
        if not self.overlays:
            return "No features added yet. Click on the image to add features!"
        
        overlay_text = "📋 Current Features (click index to remove):\n"
        overlay_text += "─" * 40 + "\n"
        for i, overlay in enumerate(self.overlays):
            overlay_text += f"[{i}] {overlay['type']:12} | x:{overlay['x']:.2f} y:{overlay['y']:.2f} | scale:{overlay['scale']:.1f}\n"
        return overlay_text
    
    def clear_all_features(self):
        """Clear all overlays"""
        self.overlays = []
        return self.render_image(), "🗑️ Cleared all features", self.get_overlay_list()
    
    def load_custom_feature(self, name, image):
        """Load a custom feature from uploaded image"""
        if image is not None and name:
            custom_img = Image.fromarray(image).convert('RGBA')
            max_size = 300
            if custom_img.width > max_size or custom_img.height > max_size:
                custom_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            feature_name = f"custom_{name}"
            self.feature_assets[feature_name] = custom_img
            return f"✅ Custom feature '{name}' loaded! Select it from the dropdown.", self.get_feature_list()
        return "Please provide both a name and an image", self.get_feature_list()
    
    def get_feature_list(self):
        """Get list of available features"""
        default_features = ["sunglasses", "glasses", "beard", "mustache", "tophat", 
                          "hair", "bowtie", "earrings", "clown_nose", "eyepatch", "monocle"]
        custom_features = [k for k in self.feature_assets.keys() if k.startswith("custom_")]
        return default_features + custom_features
    
    def render_image(self):
        """Render the image with all overlays"""
        if self.base_image is None:
            placeholder = Image.new('RGBA', (600, 400), (220, 220, 220, 255))
            draw = ImageDraw.Draw(placeholder)
            
            # Draw instructions
            draw.text((150, 180), "📤 Upload an image to start", fill=(100, 100, 100, 255))
            draw.text((120, 210), "Then click on the image to place features!", fill=(100, 100, 100, 255))
            
            return np.array(placeholder)
        
        result = self.base_image.copy()
        
        for overlay in self.overlays:
            feature = self.feature_assets.get(overlay['type'])
            if feature:
                transformed_feature = feature.copy()
                
                # Scale
                scaled_size = (
                    int(feature.width * overlay['scale']),
                    int(feature.height * overlay['scale'])
                )
                transformed_feature = transformed_feature.resize(scaled_size, Image.Resampling.LANCZOS)
                
                # Rotation
                if overlay['rotation'] != 0:
                    transformed_feature = transformed_feature.rotate(
                        -overlay['rotation'],
                        expand=True,
                        fillcolor=(0, 0, 0, 0)
                    )
                
                # Adjust opacity
                if overlay['opacity'] < 1.0:
                    alpha = transformed_feature.split()[3]
                    alpha = alpha.point(lambda p: p * overlay['opacity'])
                    transformed_feature.putalpha(alpha)
                
                # Calculate position (centered at click point)
                x = int(overlay['x'] * result.width - transformed_feature.width // 2)
                y = int(overlay['y'] * result.height - transformed_feature.height // 2)
                
                # Paste the feature
                result.paste(transformed_feature, (x, y), transformed_feature)
        
        return np.array(result)
    
    def save_image(self):
        """Save the current image"""
        if self.base_image:
            result_array = self.render_image()
            result_image = Image.fromarray(result_array)
            output_path = "/home/claude/edited_image_click.png"
            result_image.save(output_path)
            return output_path, "✅ Image saved successfully!"
        return None, "No image to save"

# Create the Gradio interface
def create_app():
    editor = ClickToPlaceEditor()
    
    with gr.Blocks(title="Click-to-Place Facial Editor", theme=gr.themes.Soft(), css="""
        .feature-button { min-height: 60px; }
        .overlay-list { font-family: monospace; }
    """) as app:
        gr.Markdown("# 🎯 Click-to-Place Facial Feature Editor")
        gr.Markdown("### 📌 Simply click on the image where you want to place features!")
        
        with gr.Row():
            # Left Column - Image Display
            with gr.Column(scale=3):
                # Main image that accepts clicks
                image_input = gr.Image(
                    label="📸 Upload & Click to Add Features",
                    type="numpy",
                    interactive=True,  # Makes it clickable
                    height=500
                )
                
                with gr.Row():
                    save_btn = gr.Button("💾 Save Image", variant="primary")
                    undo_btn = gr.Button("↩️ Undo Last", variant="secondary")
                    clear_btn = gr.Button("🗑️ Clear All", variant="stop")
                
                status = gr.Textbox(
                    label="Status", 
                    interactive=False, 
                    value="Ready! Upload an image and click to place features."
                )
            
            # Right Column - Controls
            with gr.Column(scale=1):
                gr.Markdown("### 🎨 Feature Selection")
                
                # Quick feature buttons for common items
                gr.Markdown("**Quick Select:**")
                with gr.Row():
                    quick_sunglasses = gr.Button("🕶️", elem_classes="feature-button")
                    quick_beard = gr.Button("🧔", elem_classes="feature-button")
                    quick_hat = gr.Button("🎩", elem_classes="feature-button")
                with gr.Row():
                    quick_mustache = gr.Button("👨", elem_classes="feature-button")
                    quick_glasses = gr.Button("👓", elem_classes="feature-button")
                    quick_nose = gr.Button("🔴", elem_classes="feature-button")
                
                # Dropdown for all features
                feature_dropdown = gr.Dropdown(
                    choices=editor.get_feature_list(),
                    label="Or choose from all features:",
                    value="sunglasses"
                )
                
                # Transform controls
                gr.Markdown("### ⚙️ Feature Settings")
                gr.Markdown("*Adjust before clicking to place*")
                
                scale_slider = gr.Slider(
                    minimum=0.3,
                    maximum=2.5,
                    value=1.0,
                    step=0.1,
                    label="📏 Size"
                )
                
                rotation_slider = gr.Slider(
                    minimum=-180,
                    maximum=180,
                    value=0,
                    step=5,
                    label="🔄 Rotation"
                )
                
                opacity_slider = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=1.0,
                    step=0.1,
                    label="👻 Opacity"
                )
                
                # Custom features
                with gr.Accordion("📤 Upload Custom Feature", open=False):
                    custom_name = gr.Textbox(label="Feature Name", placeholder="e.g., 'pirate_hat'")
                    custom_image = gr.Image(label="Feature Image (PNG with transparency)", type="numpy", height=150)
                    load_custom_btn = gr.Button("Add Custom Feature")
                
                # Overlay list
                gr.Markdown("### 📋 Added Features")
                overlay_list = gr.Textbox(
                    label="", 
                    lines=8, 
                    interactive=False,
                    value="No features added yet. Click on the image to add features!",
                    elem_classes="overlay-list"
                )
                
                # Remove specific overlay
                with gr.Row():
                    remove_index = gr.Number(label="Remove Index:", value=0, precision=0, scale=2)
                    remove_btn = gr.Button("❌", scale=1)
        
        # Instructions
        with gr.Accordion("📖 How to Use", open=False):
            gr.Markdown("""
            1. **Upload an image** - Drag and drop or click to browse
            2. **Select a feature** - Use quick buttons or dropdown
            3. **Adjust settings** - Size, rotation, opacity (optional)
            4. **Click on the image** - Click exactly where you want the feature
            5. **Repeat** - Add as many features as you want!
            6. **Save** - Download your masterpiece
            
            **Pro Tips:**
            - 🎯 Click precisely where you want the center of the feature
            - 🔄 Adjust rotation for tilted heads
            - 👻 Use opacity for subtle effects
            - ↩️ Undo removes the last added feature
            - 📋 Check the feature list to see all added items
            """)
        
        # Event Handlers
        
        # Handle clicks on the image
        image_input.select(
            fn=editor.handle_image_click,
            inputs=[image_input],
            outputs=[image_input, status, overlay_list]
        )
        
        # Update settings when controls change
        for control in [feature_dropdown, scale_slider, rotation_slider, opacity_slider]:
            control.change(
                fn=editor.update_settings,
                inputs=[feature_dropdown, scale_slider, rotation_slider, opacity_slider],
                outputs=[status]
            )
        
        # Quick select buttons
        quick_sunglasses.click(lambda: "sunglasses", outputs=[feature_dropdown])
        quick_beard.click(lambda: "beard", outputs=[feature_dropdown])
        quick_hat.click(lambda: "tophat", outputs=[feature_dropdown])
        quick_mustache.click(lambda: "mustache", outputs=[feature_dropdown])
        quick_glasses.click(lambda: "glasses", outputs=[feature_dropdown])
        quick_nose.click(lambda: "clown_nose", outputs=[feature_dropdown])
        
        # Load image when uploaded
        image_input.upload(
            fn=editor.load_image,
            inputs=[image_input],
            outputs=[image_input, status, overlay_list]
        )
        
        # Undo last feature
        undo_btn.click(
            fn=editor.remove_last_feature,
            inputs=[],
            outputs=[image_input, status, overlay_list]
        )
        
        # Clear all
        clear_btn.click(
            fn=editor.clear_all_features,
            inputs=[],
            outputs=[image_input, status, overlay_list]
        )
        
        # Save image
        save_btn.click(
            fn=editor.save_image,
            inputs=[],
            outputs=[gr.File(label="Download"), status]
        )
        
        # Load custom feature
        load_custom_btn.click(
            fn=editor.load_custom_feature,
            inputs=[custom_name, custom_image],
            outputs=[status, feature_dropdown]
        )
        
        # Remove specific overlay
        remove_btn.click(
            fn=editor.remove_overlay_by_index,
            inputs=[remove_index],
            outputs=[image_input, status, overlay_list]
        )
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True, debug=True)
