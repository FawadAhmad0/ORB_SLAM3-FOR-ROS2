#!/bin/bash
# Script to run ORB-SLAM3 on the OmniSLAM dataset using ONLY depth images

ORB_SLAM3_DIR="/home/romi/fawad/ORB_SLAM3"
DATASET_DIR="/home/romi/fawad/back"

echo "Running ORB-SLAM3 Monocular on DEPTH images only..."

# Provide the libraries path
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORB_SLAM3_DIR/lib:$ORB_SLAM3_DIR/Thirdparty/DBoW2/lib:$ORB_SLAM3_DIR/Thirdparty/g2o/lib:$ORB_SLAM3_DIR/Thirdparty/Sophus/install/lib

# mono_tum expects rgb.txt to exist. We will safely copy our depth_association.txt to rgb.txt temporarily
cp $DATASET_DIR/depth_association.txt $DATASET_DIR/rgb.txt

# Execute the Monocular TUM example
$ORB_SLAM3_DIR/Examples/Monocular/mono_tum \
    $ORB_SLAM3_DIR/Vocabulary/ORBvoc.txt \
    $DATASET_DIR/OmniSLAM_depth.yaml \
    $DATASET_DIR

# Clean up the temporary rgb.txt file
rm $DATASET_DIR/rgb.txt
