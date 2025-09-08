import PyInstaller.__main__
import os
import sys

def build_executable():
    """Build the executable using PyInstaller"""
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # PyInstaller arguments
    args = [
        'converter.py',  # Main script
        '--onefile',     # Create a single executable file
        '--windowed',    # Hide console window (GUI app)
        '--name=URLConverter',  # Name of the executable
        '--icon=icon.ico',  # Icon file (if exists)
        '--version-file=version_info.txt',  # Version information
        '--add-data=requirements.txt;.',  # Include requirements.txt
        '--hidden-import=yt_dlp',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--clean',       # Clean cache and temporary files
        '--noconfirm',   # Replace output directory without asking
        '--uac-admin',   # Request admin privileges
    ]
    
    # Remove icon argument if icon file doesn't exist
    if not os.path.exists(os.path.join(current_dir, 'icon.ico')):
        args = [arg for arg in args if not arg.startswith('--icon')]
    
    print("Building executable...")
    print(f"Arguments: {' '.join(args)}")
    
    try:
        PyInstaller.__main__.run(args)
        print("\nBuild completed successfully!")
        print(f"Executable location: {os.path.join(current_dir, 'dist', 'URLConverter.exe')}")
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()

