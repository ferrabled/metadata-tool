# Metadata Tool
<img src="https://github.com/ferrabled/metadata-tool/assets/48551658/f7c61af3-2ebc-41c4-bd79-a818efaf8e48" width="200" height="200">

## Introduction

The Metadata Tool is a Python script designed to read and manage metadata from image files in a specified directory and its subdirectories. It allows you to retrieve and display metadata information for image files, including details like camera settings, image descriptions, and more.


## Features

- Read and display metadata from image files.
- Delete metadata from files inside a folder.
- Handle various image formats, including JPEG and PNG.
- Automatically traverse through specified directories and subdirectories.
- Identify and handle cases where metadata is missing or empty.
- Easy to use command-line interface.

## Requirements

The requirements (PIL) can be installed with 
 ```bash
pip install -r 'requirements.txt'
```


## Usage

To use the Metadata Tool, follow these steps:

1. Clone or download the tool from the [GitHub repository](https://github.com/ferrabled/metadata-tool).

2. Navigate to the tool's directory using the command line.

3. Run the tool by executing the script:
  ```bash
  python metadatatool.py
  ```

4. You will be prompted to enter the path of the folder containing the images from which you want to retrieve metadata. Then press Enter.

5. The tool will provide diferent options. Select the desired one.

6. The tool will start processing the images and display metadata information for each image found.

7. Metadata is displayed in the format `TagName: Value`. Tags with no metadata will be displayed as `TagName: None`.

8. If you selected to export the metadata it would be saved into `metadata.csv`.


## Examples

Here are some example usages of the Metadata Tool:

- Retrieve metadata from images in a specific folder:

Select the file to read: /path/to/your/image/folder

- View metadata for each image in the specified folder and its subfolders.


## Troubleshooting

If you encounter any issues or errors, feel free to open an issue.
Also consider the following:

- Ensure that you have provided the correct path to the image folder.
- Verify that the Pillow (PIL) library is installed.


