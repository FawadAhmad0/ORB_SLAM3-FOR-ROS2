import os

def main():
    base_dir = "/home/romi/fawad/back"
    rgb_dir = os.path.join(base_dir, "rgb")
    depth_dir = os.path.join(base_dir, "depth")
    
    # We need timestamps. We get them from the RGB filenames
    rgb_files = sorted(os.listdir(rgb_dir))
    depth_files = sorted(os.listdir(depth_dir))
    
    num_frames = min(len(rgb_files), len(depth_files))
    
    association_file = os.path.join(base_dir, "depth_association.txt")
    with open(association_file, 'w') as f:
        # TUM Monocular looks for a file with format: timestamp filename
        # It expects an rgb.txt file, but we will point it to depth files
        for i in range(num_frames):
            rgb_name = rgb_files[i]
            depth_name = depth_files[i]
            
            # Timestamp from rgb name
            timestamp = os.path.splitext(rgb_name)[0]
            
            # format: timestamp depth_file
            f.write(f"{timestamp} depth/{depth_name}\n")
            
    print(f"Successfully created {association_file} for depth-only tracking with {num_frames} frames.")

if __name__ == "__main__":
    main()
