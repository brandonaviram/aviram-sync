#!/usr/bin/env python3
"""
Minimalist Travel Media Sync Tool
A simple rsync-based tool for syncing photos and videos from memory cards
Organizes files by location, date, and media type for travel campaigns
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform
from datetime import datetime
import argparse

class MediaSyncTool:
    def __init__(self, breakout=False, debug_mode=False):
        self.video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.m4v', '.wmv', '.flv', '.webm', '.3gp'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
            '.raw', '.cr2', '.cr3', '.nef', '.arw', '.dng', '.heic', '.webp', '.3fr', '.ari', '.srf', '.sr2', '.bay', '.braw', '.cap', '.data', '.dcs', '.dcr', '.drf', '.eip', '.erf', '.fff', '.gpr', '.iiq', '.k25', '.kdc', '.mdc', '.mef', '.mos', '.mrw', '.nrw', '.obm', '.orf', '.pef', '.ptx', '.pxn', '.r3d', '.raf', '.rwl', '.rw2', '.rwz', '.srw', '.x3f'}
        self.debug_mode = debug_mode
        self.breakout = breakout
        
    def check_rsync_installed(self):
        """Check if rsync is installed on the system"""
        return shutil.which('rsync') is not None
    
    def install_rsync(self):
        """Install rsync based on the operating system"""
        system = platform.system().lower()
        
        print("rsync not found. Installing...")
        
        try:
            if system == 'darwin':  # macOS
                # Try homebrew first, then macports
                if shutil.which('brew'):
                    subprocess.run(['brew', 'install', 'rsync'], check=True)
                elif shutil.which('port'):
                    subprocess.run(['sudo', 'port', 'install', 'rsync'], check=True)
                else:
                    print("Please install Homebrew or MacPorts to automatically install rsync")
                    print("Or install rsync manually: https://rsync.samba.org/")
                    return False
                    
            elif system == 'linux':
                # Try different package managers
                if shutil.which('apt-get'):
                    subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'rsync'], check=True)
                elif shutil.which('yum'):
                    subprocess.run(['sudo', 'yum', 'install', '-y', 'rsync'], check=True)
                elif shutil.which('dnf'):
                    subprocess.run(['sudo', 'dnf', 'install', '-y', 'rsync'], check=True)
                elif shutil.which('pacman'):
                    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'rsync'], check=True)
                else:
                    print("Please install rsync using your system's package manager")
                    return False
                    
            elif system == 'windows':
                print("Windows detected. Please install rsync manually:")
                print("1. Install Windows Subsystem for Linux (WSL)")
                print("2. Or use Cygwin with rsync package")
                print("3. Or download rsync for Windows from https://rsync.samba.org/")
                return False
                
            else:
                print(f"Unsupported operating system: {system}")
                return False
                
            print("rsync installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to install rsync: {e}")
            return False
    
    def is_media_file(self, file_path):
        """Check if a file is a video or image file"""
        extension = file_path.suffix.lower()
        is_media = extension in self.video_extensions or extension in self.image_extensions
        if self.debug_mode:
            print(f"[DEBUG] Checking file: {file_path.name} (ext: {extension}) -> {'MEDIA' if is_media else 'SKIP'}")
        return is_media
    
    def get_media_files(self, source_dir):
        """Get list of all media files in source directory"""
        if self.debug_mode:
            print(f"[DEBUG] get_media_files called, debug_mode={self.debug_mode}")
            print(f"[DEBUG] Source directory: {source_dir}")
        
        media_files = []
        source_path = Path(source_dir)
        
        if not source_path.exists():
            print(f"Source directory does not exist: {source_dir}")
            return media_files
        
        if self.debug_mode:
            print(f"[DEBUG] Scanning directory recursively...")
            all_files = list(source_path.rglob('*'))
            print(f"[DEBUG] Found {len(all_files)} total files/directories")
            
            # Show first 20 files for debugging
            files_only = [f for f in all_files if f.is_file()]
            print(f"[DEBUG] Found {len(files_only)} files (excluding directories)")
            print(f"[DEBUG] First 20 files:")
            for i, f in enumerate(files_only[:20]):
                print(f"  {i+1}. {f.name} (ext: {f.suffix.lower()})")
            if len(files_only) > 20:
                print(f"  ... and {len(files_only) - 20} more files")
            print("")
        
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and self.is_media_file(file_path):
                media_files.append(file_path)
        
        if self.debug_mode:
            print("\n[DEBUG] Media files found:")
            for f in media_files:
                print(f"  {f} (.{f.suffix.lower()[1:]})")
            print(f"[DEBUG] Total media files: {len(media_files)}\n")
        
        return media_files
    
    def create_file_list(self, media_files, temp_file):
        """Create a temporary file list for rsync --files-from"""
        with open(temp_file, 'w') as f:
            for file_path in media_files:
                # Write relative path from source directory
                f.write(str(file_path) + '\n')
    
    def sync_media(self, source_dir, dest_dir, location_name):
        """Sync media files using rsync with organized folder structure"""
        source_path = Path(source_dir)
        
        # Create formatted folder name: "LOCATION JUNE 2025" (all caps)
        current_date = datetime.now()
        month_year = current_date.strftime("%B %Y").upper()  # e.g., "JUNE 2025"
        formatted_location = location_name.upper()  # All caps
        main_folder_name = f"{formatted_location} {month_year}"  # Space instead of dash
        
        dest_path = Path(dest_dir) / main_folder_name
        
        # Get all media files
        media_files = self.get_media_files(source_dir)
        
        if not media_files:
            print("No media files found in source directory")
            return False
        
        print(f"Found {len(media_files)} media files")
        
        # Separate files by type
        video_files = [f for f in media_files if f.suffix.lower() in self.video_extensions]
        image_files = [f for f in media_files if f.suffix.lower() in self.image_extensions]
        
        # Create organized directory structure (all caps)
        videos_dest = dest_path / "VIDEOS"
        images_dest = dest_path / "IMAGES"
        
        videos_dest.mkdir(parents=True, exist_ok=True)
        images_dest.mkdir(parents=True, exist_ok=True)
        
        print(f"Organizing into: {dest_path}")
        print(f"  Videos: {len(video_files)} files → VIDEOS/")
        print(f"  Images: {len(image_files)} files → IMAGES/")
        
        success = True
        
        # Sync videos
        if video_files:
            print("\nSyncing videos...")
            if not self._sync_file_list(video_files, videos_dest):
                success = False
        
        # Sync images  
        if image_files:
            print("\nSyncing images...")
            if self.breakout:
                from collections import defaultdict
                img_types = defaultdict(list)
                for img in image_files:
                    img_types[img.suffix.lower()].append(img)
                for ext, files in img_types.items():
                    ext_folder = images_dest / ext[1:].upper()
                    ext_folder.mkdir(parents=True, exist_ok=True)
                    print(f"  {ext[1:].upper()}: {len(files)} files → {ext_folder}/")
                    if not self._sync_file_list(files, ext_folder):
                        success = False
            else:
                if not self._sync_file_list(image_files, images_dest):
                    success = False
        
        if success:
            print(f"\nSync completed successfully!")
            print(f"Files organized in: {dest_path}")
            print(f"  📁 Videos: {videos_dest}")
            print(f"  📁 Images: {images_dest}")
        
        return success
    
    def _sync_file_list(self, file_list, dest_dir):
        """Sync a list of files to destination, flattening the structure"""
        rsync_cmd = [
            'rsync',
            '-avh',  # archive, verbose, human-readable
            '--progress',  # show progress
        ]
        
        # Add each file individually (flattens structure)
        for media_file in file_list:
            rsync_cmd.append(str(media_file))
        
        # Add destination
        rsync_cmd.append(str(dest_dir) + "/")
        
        try:
            subprocess.run(rsync_cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Sync failed: {e}")
            return False
    
    def get_user_input(self):
        """Get source directory, destination directory, and folder name from user"""
        print("=== Travel Media Sync Tool ===\n")
        
        # Get source directory with default
        while True:
            print("Tip: Press Enter to use default '/Volumes/Untitled' or enter custom path")
            source_input = input("Source directory [/Volumes/Untitled]: ").strip()
            
            # Use default if empty
            if not source_input:
                source = "/Volumes/Untitled"
            else:
                # Remove surrounding quotes if present
                if source_input.startswith('"') and source_input.endswith('"'):
                    source = source_input[1:-1]
                elif source_input.startswith("'") and source_input.endswith("'"):
                    source = source_input[1:-1]
                else:
                    source = source_input
            
            source_path = Path(source)
            if not source_path.exists():
                print(f"Directory does not exist: {source}")
                print("Make sure your memory card is mounted and the path is correct.\n")
                continue
            
            if not source_path.is_dir():
                print(f"Path is not a directory: {source}\n")
                continue
            
            break
        
        # Get destination directory with Movies/Photos choice
        while True:
            print("\nChoose destination:")
            print("1. Movies folder (~/Movies)")
            print("2. Photos folder (~/Pictures)")
            print("3. Custom path")
            
            choice = input("Choice [1]: ").strip()
            
            if not choice or choice == "1":
                dest = str(Path.home() / "Movies")
            elif choice == "2":
                dest = str(Path.home() / "Pictures")
            elif choice == "3":
                dest_input = input("Enter custom destination path: ").strip()
                # Remove surrounding quotes if present
                if dest_input.startswith('"') and dest_input.endswith('"'):
                    dest = dest_input[1:-1]
                elif dest_input.startswith("'") and dest_input.endswith("'"):
                    dest = dest_input[1:-1]
                else:
                    dest = dest_input
            else:
                print("Invalid choice. Please enter 1, 2, or 3.\n")
                continue
                
            if not dest:
                print("Destination directory cannot be empty\n")
                continue
            
            dest_path = Path(dest)
            if dest_path.exists() and not dest_path.is_dir():
                print(f"Path exists but is not a directory: {dest}\n")
                continue
            
            break
        
        # Get folder name
        while True:
            location_name = input("\nEnter location/shoot name: ").strip()
            if not location_name:
                print("Location name cannot be empty")
                continue
            # Check for invalid characters
            invalid_chars = '<>:"/\\|?*'
            if any(char in location_name for char in invalid_chars):
                print(f"Location name contains invalid characters: {invalid_chars}")
                continue
            break
        return source, dest, location_name
    
    def preview_sync(self, source_dir, location_name):
        """Show preview of what files will be synced"""
        media_files = self.get_media_files(source_dir)
        
        if not media_files:
            print("No media files found")
            return
        
        # Create formatted folder name preview (all caps)
        current_date = datetime.now()
        month_year = current_date.strftime("%B %Y").upper()
        formatted_location = location_name.upper()
        main_folder_name = f"{formatted_location} {month_year}"  # Space instead of dash
        
        print(f"\nPreview - Found {len(media_files)} media files:")
        print(f"Will organize into: {main_folder_name}/")
        
        # Group by type
        videos = [f for f in media_files if f.suffix.lower() in self.video_extensions]
        images = [f for f in media_files if f.suffix.lower() in self.image_extensions]
        
        if videos:
            print(f"\n📹 Videos ({len(videos)}) → VIDEOS/:")
            for video in videos[:5]:  # Show first 5
                print(f"  {video.name}")
            if len(videos) > 5:
                print(f"  ... and {len(videos) - 5} more")
        
        if images:
            # Group images by extension
            from collections import defaultdict
            img_types = defaultdict(list)
            for img in images:
                img_types[img.suffix.lower()].append(img)
            print(f"\n📸 Images (total: {len(images)})")
            for ext, files in sorted(img_types.items()):
                print(f"  - {ext[1:].upper()}: {len(files)} files")
                for image in files[:2]:
                    print(f"    {image.name}")
                if len(files) > 2:
                    print(f"    ... and {len(files) - 2} more")
            if self.breakout:
                print("  (Will organize by type: IMAGES/JPG/, IMAGES/RAF/, etc.)")
            else:
                print("  (All images will go into IMAGES/)")
    
    def run(self):
        """Main application loop"""
        if self.debug_mode:
            print("[DEBUG] *** DEBUG MODE ENABLED ***")
            print(f"[DEBUG] self.debug_mode = {self.debug_mode}")
            print(f"[DEBUG] self.breakout = {self.breakout}")
        
        # Check if rsync is installed
        if not self.check_rsync_installed():
            if not self.install_rsync():
                print("rsync is required but could not be installed. Exiting.")
                sys.exit(1)
        
        try:
            # Get user input
            source, dest, location_name = self.get_user_input()
            
            # Show preview
            print("\n" + "="*50)
            self.preview_sync(source, location_name)
            
            # Show final destination preview
            current_date = datetime.now()
            month_year = current_date.strftime("%B %Y").upper()
            formatted_location = location_name.upper()
            main_folder_name = f"{formatted_location} {month_year}"  # Space instead of dash
            final_dest = Path(dest) / main_folder_name
            
            # Confirm before proceeding
            print("\n" + "="*50)
            print(f"Source: {source}")
            print(f"Destination: {final_dest}")
            print(f"  📁 Videos → {final_dest}/VIDEOS/")
            print(f"  📁 Images → {final_dest}/IMAGES/")
            
            confirm = input("\nProceed with sync? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("Sync cancelled")
                return
            
            # Perform sync
            success = self.sync_media(source, dest, location_name)
            
            if success:
                print("\n" + "="*50)
                print("Backup completed successfully! 🎉")
            else:
                print("\n" + "="*50)
                print("Backup failed! ❌")
                
        except KeyboardInterrupt:
            print("\n\nSync cancelled by user")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description="Minimalist Travel Media Sync Tool")
    parser.add_argument('--breakout', action='store_true', help='Organize images by type (e.g., IMAGES/RAF/, IMAGES/JPG/)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for detailed output')
    args = parser.parse_args()
    app = MediaSyncTool(breakout=args.breakout, debug_mode=args.debug)
    app.run()

if __name__ == "__main__":
    main()