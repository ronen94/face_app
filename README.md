# Facial Feature Editor - Gradio App

A fun interactive web application for adding facial features and accessories to photos using Gradio.

## 🎯 Quick Start - Which Version Should I Use?

| Version | Best For | Key Feature | Difficulty |
|---------|----------|-------------|------------|
| **interactive_facial_editor.py** | Best overall experience | Click to place + 15+ features | ⭐ Easiest |
| **click_to_place_editor.py** | Simple and intuitive | Click to place features | ⭐ Easy |
| **advanced_facial_editor.py** | Power users | Full control with sliders | ⭐⭐ Medium |
| **facial_editor_app.py** | Learning/basic use | Simple slider controls | ⭐⭐ Medium |

**Recommendation:** Start with `interactive_facial_editor.py` for the best experience!

## Available Versions

### 1. Basic Version (`facial_editor_app.py`)
- Upload any photo as base image
- Add pre-made facial features (beard, mustache, sunglasses, hat, etc.)
- Control position with sliders and scale of each feature
- Simple and easy-to-use interface
- Save edited images

### 2. Advanced Version (`advanced_facial_editor.py`)
- All basic features plus:
- **Custom feature upload**: Upload your own PNG images as features
- **Rotation control**: Rotate features at any angle
- **Opacity control**: Adjust transparency of overlays
- **Advanced overlay management**: Update or remove specific overlays
- **Better feature designs**: More realistic default features
- **Multiple tabs** for built-in and custom features
- Uses sliders for positioning

### 3. Click-to-Place Version (`click_to_place_editor.py`) ⭐ NEW!
- **Click directly on the image** to place features - no sliders needed!
- Quick select buttons with emoji icons
- Real-time feature list display
- Undo/redo functionality
- Custom feature support
- More intuitive interaction

### 4. Interactive Version (`interactive_facial_editor.py`) ⭐ NEWEST!
- **Most advanced click-to-place interface**
- Enhanced visual feedback
- Extended feature library (15+ items)
- Professional-looking default features
- Improved quick-select palette
- Better organized UI

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Basic Version (Slider-based):
```bash
python facial_editor_app.py
```

### Running the Advanced Version (Slider-based with more features):
```bash
python advanced_facial_editor.py
```

### Running the Click-to-Place Version (Recommended for ease of use):
```bash
python click_to_place_editor.py
```

### Running the Interactive Version (Most feature-rich):
```bash
python interactive_facial_editor.py
```

The app will launch in your browser. If not, check the terminal for the local URL (usually `http://127.0.0.1:7860`).

## How to Use

### Click-to-Place Workflow (Recommended - versions 3 & 4):
1. **Upload an image**: Click on the image area or drag-drop a photo
2. **Select a feature**: Use quick emoji buttons or dropdown menu
3. **Adjust settings** (optional): Set size, rotation, opacity before clicking
4. **Click on the image**: Click exactly where you want the feature placed
5. **Repeat**: Keep clicking to add more features
6. **Save**: Download your creation

### Slider-based Workflow (versions 1 & 2):
1. **Upload an image**: Click on the image upload area or drag-drop a photo
2. **Select a feature**: Choose from the available facial features in the toolbar
3. **Position the feature**: Use X and Y sliders to position it
4. **Adjust size**: Use the scale slider to resize
5. **Add the feature**: Click "Add Feature" to place it on the image
6. **Repeat**: Add as many features as you want
7. **Save**: Click "Save Image" to download your creation

### Advanced Features (Advanced Version Only):

#### Adding Custom Features:
1. Go to the "Custom Feature" tab
2. Enter a name for your feature
3. Upload a PNG image (preferably with transparency)
4. Click "Load Custom Feature"
5. Your feature will be available in the dropdown

#### Editing Existing Overlays:
1. Check the "Overlay List" to see numbered overlays
2. Enter the overlay index number
3. Adjust the transform controls
4. Click "Update Overlay" to apply changes

## Supported Features

### Built-in Features:
- 👓 Sunglasses
- 🤓 Glasses
- 🧔 Beard
- 👨 Mustache
- 🎩 Top Hat
- 💇 Hair/Wig
- 🎀 Bow Tie
- 💍 Earrings
- 🔴 Clown Nose
- 🏴‍☠️ Eye Patch

### Custom Features:
Upload any PNG image with transparency for best results. Recommended size: 100-300 pixels.

## Tips for Best Results

1. **Use high-quality base images** for better results
2. **PNG with transparency** work best for custom features
3. **Start with larger scale** and adjust down as needed
4. **Layer order matters**: Features are added in the order you place them
5. **Use opacity** to blend features more naturally
6. **Rotation** can help align features with face angle

## Troubleshooting

**Issue**: Features appear pixelated
- **Solution**: Use higher resolution custom feature images

**Issue**: Features don't align properly
- **Solution**: Adjust both X/Y position and rotation for better alignment

**Issue**: App won't start
- **Solution**: Ensure all dependencies are installed and Python version is 3.8+

**Issue**: Custom features not loading
- **Solution**: Ensure the image is in a supported format (PNG, JPG) and not too large (>5MB)

## Technical Details

- Built with **Gradio** for the web interface
- Uses **Pillow (PIL)** for image processing
- **NumPy** for array operations
- Supports RGBA for transparency
- Real-time preview of changes

## Future Enhancements Ideas

- Face detection for automatic positioning
- More built-in features
- Feature animation support
- Batch processing
- Social media integration
- AI-powered feature suggestions

## License

Free to use and modify for personal and educational purposes.

---

Have fun creating hilarious and creative photo edits! 🎨📸
