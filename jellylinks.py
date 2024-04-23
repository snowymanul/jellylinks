import os
import sys

def create_hardlinks(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.mkv', '.mp4', '.avi')):
                video_file = os.path.join(root, file)
                video_name, _ = os.path.splitext(file)

                # Search for audio tracks and subtitles in the same directory and subdirectories
                for subdir, _, subfiles in os.walk(root):
                    for f in subfiles:
                        if f.startswith(video_name):
                            if f.endswith('.mka') or f.endswith('.ass') or f.endswith('.srt'):
                                # Create hard link next to the video file with folder name as extension
                                source_path = os.path.join(subdir, f)
                                subdir_name = os.path.basename(os.path.dirname(source_path))
                                hardlink_name = f"{os.path.splitext(file)[0]}.{subdir_name}.{os.path.splitext(f)[1][1:]}"
                                
                                # Check if the hard link already exists
                                if not os.path.exists(os.path.join(os.path.dirname(video_file), hardlink_name)):
                                    os.link(source_path, os.path.join(os.path.dirname(video_file), hardlink_name))
                                    print(f"Hard link created: {hardlink_name}")
                                else:
                                    print(f"Hard link already exists: {hardlink_name}")

# Check if at least one argument is provided
if len(sys.argv) < 2:
    print("Usage: python3 run.py '/path/to/folder'")
    sys.exit(1)

# Get the folder path from command line argument
folder_path = sys.argv[1]

# Check if the folder exists
if os.path.isdir(folder_path):
    # Call the function to create hard links
    create_hardlinks(folder_path)
else:
    print("Invalid folder path.")
