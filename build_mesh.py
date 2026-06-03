import open3d as o3d
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R
import os

# --- 1. YOUR CUSTOM DATA PATHS (UPDATE THESE) ---
RGB_FOLDER = "/home/romi/farhan/omnislam dataset/0/bottom/rgb/"
DEPTH_FOLDER = "/home/romi/farhan/omnislam dataset/0/bottom/depth/"
POSE_FILE = "/home/romi/farhan/omnislam dataset/0/bottom/bottom_groundtruth.txt"

# --- 2. YOUR CAMERA INTRINSICS (UPDATE THESE) ---
# You must input the focal length (fx, fy) and optical center (cx, cy) of the camera that took the images.
# If you don't know them, 525.0 and 320/240 is a common default for standard 640x480 depth cameras.
width = 640
height = 480
fx = 525.0
fy = 525.0
cx = 319.5
cy = 239.5
intrinsic = o3d.camera.PinholeCameraIntrinsic(width, height, fx, fy, cx, cy)

# --- 3. INITIALIZE 3D VOLUME ---
# This voxel length controls the resolution of your mesh (smaller = better quality but uses more RAM)
volume = o3d.pipelines.integration.ScalableTSDFVolume(
    voxel_length=0.02,
    sdf_trunc=0.04,
    color_type=o3d.pipelines.integration.TSDFVolumeColorType.RGB8)

print("Reading poses and fusing frames. This may take a few minutes...")

# Read poses
with open(POSE_FILE, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    parts = line.strip().split()
    if len(parts) < 7: continue # Skip empty lines
    
    # Assuming TUM format: timestamp tx ty tz qx qy qz qw
    # If your file doesn't have a timestamp at the start, adjust the indices!
    timestamp = parts[0]
    tx, ty, tz = float(parts[1]), float(parts[2]), float(parts[3])
    qx, qy, qz, qw = float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])
    
    # Construct 4x4 Camera-to-World transformation matrix
    pose_matrix = np.eye(4)
    pose_matrix[:3, :3] = R.from_quat([qx, qy, qz, qw]).as_matrix()
    pose_matrix[:3, 3] = [tx, ty, tz]
    
    # Open3D requires the World-to-Camera extrinsic matrix, which is the inverse of Camera-to-World
    extrinsic = np.linalg.inv(pose_matrix)
    
    # Load RGB and Depth (Assuming filenames match the timestamp or are sequential)
    # UPDATE these lines if your filenames are named differently (e.g. 0001.png instead of timestamp)
    color_path = os.path.join(RGB_FOLDER, f"{timestamp}.png")
    depth_path = os.path.join(DEPTH_FOLDER, f"{timestamp}.png")
    
    if not os.path.exists(color_path) or not os.path.exists(depth_path):
        continue
        
    color = o3d.io.read_image(color_path)
    # Assuming depth is 16-bit PNG in millimeters. 
    depth = o3d.io.read_image(depth_path)
    
    rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color, depth, depth_scale=1000.0, depth_trunc=3.0, convert_rgb_to_intensity=False)
    
    # Integrate into the 3D volume
    volume.integrate(rgbd, intrinsic, extrinsic)
    
    if i % 50 == 0:
        print(f"Fused {i} frames...")

# --- 4. EXTRACT AND SAVE MESH ---
print("Extracting 3D Mesh...")
mesh = volume.extract_triangle_mesh()
mesh.compute_vertex_normals()
o3d.io.write_triangle_mesh("custom_scene.ply", mesh)
print("Success! Saved as custom_scene.ply")
