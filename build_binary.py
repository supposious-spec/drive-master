#!/usr/bin/env python3
"""
Build script to create standalone binary for Drive Master
"""
import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_binary():
    """Build standalone binary"""
    print("🔨 Building standalone binary...")
    
    # PyInstaller command to create single file executable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "drive-master",
        "--console",
        "--clean",
        "mount_drive.py"
    ]
    
    subprocess.check_call(cmd)
    print("✅ Binary created in dist/drive-master")

def main():
    install_pyinstaller()
    build_binary()
    
    print("\n🎉 Build complete!")
    print("📁 Binary location: dist/drive-master")
    print("🚀 Test it: ./dist/drive-master --version")

if __name__ == "__main__":
    main()