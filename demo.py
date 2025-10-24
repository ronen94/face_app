#!/usr/bin/env python3
"""
Quick Demo Script for Facial Feature Editor
Tests the click-to-place functionality
"""

import sys
import os

def print_banner():
    print("=" * 60)
    print("🎭 FACIAL FEATURE EDITOR - CLICK TO PLACE DEMO 🎭")
    print("=" * 60)
    print()

def main():
    print_banner()
    
    print("Available versions to run:")
    print()
    print("1. Interactive Editor (RECOMMENDED - Best click-to-place)")
    print("2. Click-to-Place Editor (Good click-to-place)")  
    print("3. Advanced Editor (Slider-based with all features)")
    print("4. Basic Editor (Simple slider-based)")
    print()
    
    choice = input("Enter your choice (1-4) or 'q' to quit: ").strip()
    
    scripts = {
        "1": "interactive_facial_editor.py",
        "2": "click_to_place_editor.py",
        "3": "advanced_facial_editor.py",
        "4": "facial_editor_app.py"
    }
    
    if choice.lower() == 'q':
        print("Goodbye!")
        sys.exit(0)
    
    if choice in scripts:
        script = scripts[choice]
        print(f"\n✅ Launching {script}...")
        print("\n📝 Instructions for click-to-place versions:")
        print("   1. Upload your photo")
        print("   2. Select a feature from the toolbar")
        print("   3. Click directly on the image where you want it!")
        print("   4. Adjust size/rotation as needed")
        print("   5. Save your masterpiece!")
        print("\n🌐 Opening in browser...\n")
        
        os.system(f"python {script}")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bye! Thanks for using Facial Feature Editor!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have installed the requirements:")
        print("  pip install -r requirements.txt")
