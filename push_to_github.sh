#!/bin/bash

# Navigate to the main directory
cd /home/romi/fawad

echo "Configuring GitHub remote..."
git remote remove origin 2>/dev/null

# Force Git to use your username (FawadAhmad0) instead of the cached Farhan3376
REPO_URL="https://FawadAhmad0@github.com/FawadAhmad0/ORB_SLAM3-FOR-ROS2.git"
git remote add origin $REPO_URL

echo "Pushing all files to $REPO_URL ..."
echo "--------------------------------------------------------"
echo "IMPORTANT: GitHub no longer accepts account passwords."
echo "When prompted for a password for 'https://FawadAhmad0@github.com', "
echo "you MUST paste your GitHub Personal Access Token (PAT)."
echo "--------------------------------------------------------"

# Push to the master branch (force push to overwrite the initial GitHub commit)
git push -f -u origin master

