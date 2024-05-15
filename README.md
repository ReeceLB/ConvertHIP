# Houdini Absolute to Relative Path Converter

## Introduction
This Houdini shelf tool is designed to find nodes with absolute file paths and convert them to relative paths based on the $HIP directory. It provides a convenient way to manage file paths within your Houdini project.

## Features
- Find Absolute Paths: Displays a list of nodes with absolute file paths.
- Find Relative Path: Shows the relative paths based on the $HIP and $HOME directories.
- Copy and Convert: Copies files to relevant folders and converts file paths to the relative $HIP directory.

## Usage
1. 1. Click on the "ConvertHIP" tool on your Houdini shelf.
2. Use the "Find Absolute Paths" button to identify nodes with absolute file paths.
3. Utilize the "Find Relative Path" button to view the project's HIP and HOME directories.
4. Click on "Copy and Convert" to copy files to relevant project folders and update paths.
Can also watch the Usability video.

## Installation
1. Watch Installation video.

## Compatibility
- Tested on Houdini [20.0.547].
- Compatible with PySide2.

## Notes
- Supported file extensions: .jpeg, .jpg, .png, .exr, .hdr, .tif, .targa, .obj, .fbx, .abc, .bgeo, .bgeo.sc, .geo, .vdb.
- Excluded file extensions: .cl (customize in the script if needed).
