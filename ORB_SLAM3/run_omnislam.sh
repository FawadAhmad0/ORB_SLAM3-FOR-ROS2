#!/bin/bash
# Script to run ORB-SLAM3 on the OmniSLAM dataset

ORB_SLAM3_DIR="/home/romi/fawad/ORB_SLAM3"
DATASET_DIR="/home/romi/fawad/back"

echo "Running ORB-SLAM3 RGB-D on OmniSLAM Dataset..."
echo "Using ORB-SLAM3 at: $ORB_SLAM3_DIR"
echo "Dataset at: $DATASET_DIR"

# Provide the libraries path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORB_SLAM3_DIR/lib:$ORB_SLAM3_DIR/Thirdparty/DBoW2/lib:$ORB_SLAM3_DIR/Thirdparty/g2o/lib:$ORB_SLAM3_DIR/Thirdparty/Sophus/install/lib

# Execute the RGB-D TUM example
$ORB_SLAM3_DIR/Examples/RGB-D/rgbd_tum \
    $ORB_SLAM3_DIR/Vocabulary/ORBvoc.txt \
    $DATASET_DIR/OmniSLAM.yaml \
    $DATASET_DIR \
    $DATASET_DIR/associations.txt
