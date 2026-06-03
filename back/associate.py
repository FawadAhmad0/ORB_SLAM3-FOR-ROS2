import os
import glob

def main():
    base_dir = "/home/romi/fawad/back"
    rgb_dir = os.path.join(base_dir, "rgb")
    depth_dir = os.path.join(base_dir, "depth")
    
    # Get sorted list of files
    rgb_files = sorted(os.listdir(rgb_dir))
    depth_files = sorted(os.listdir(depth_dir))
    
    if len(rgb_files) != len(depth_files):
        print(f"WARNING: Number of RGB files ({len(rgb_files)}) does not match Depth files ({len(depth_files)}).")
        print("Association will be truncated to the shortest list.")
        
    num_frames = min(len(rgb_files), len(depth_files))
    
    association_file = os.path.join(base_dir, "associations.txt")
    with open(association_file, 'w') as f:
        for i in range(num_frames):
            rgb_name = rgb_files[i]
            depth_name = depth_files[i]
            
            # The timestamp is the filename of the rgb image without extension
            timestamp = os.path.splitext(rgb_name)[0]
            
            # TUM format: timestamp rgb_file timestamp depth_file
            f.write(f"{timestamp} rgb/{rgb_name} {timestamp} depth/{depth_name}\n")
            
    print(f"Successfully created {association_file} with {num_frames} associations.")

if __name__ == "__main__":
    main()
