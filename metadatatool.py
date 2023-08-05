import os
import sys
from PIL import Image, ExifTags

def init_menu():
    # Set up the menu, the user should select which option to run
    print("1) Read metadata")
    print("2) Read & Export metadata")
    print("3) Delete metadata")
    print("4) Exit")
    print("Select an option: ")
    option = input()
    return option


def read_metadata():
    # Read metadata from a file
    # The user should select the file to read
    print("Select the file to read: ")
    file_path = input()
    # Check if the file exists
    if os.path.isdir(file_path):
        print("Looking for images in: " + file_path)
        # Read the metadata
        for file in os.listdir(file_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                print("Image found: " + file)
                image = Image.open(os.path.join(file_path, file))
                exifdata = image.getexif()
                if(len(exifdata)>0):
                    exif = { ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS }
                    # Print the metadata
                    print(exif)
                else:
                    print("{ No metadata found for this image }")
    else:
        print("The file does not exist")


def main():
    # Main function
    # Set up the menu
    option = init_menu()
    # Check the option selected by the user
    if option == "1":
        # Read metadata
        read_metadata()
    elif option == "3":
        # Exit
        print("Exiting")
        sys.exit()
    else:
        print("Invalid option")
        sys.exit()

    
if __name__ == "__main__":
    main()

    
