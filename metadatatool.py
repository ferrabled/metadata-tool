import os
import sys
from PIL import Image, ExifTags

def init_menu():
    # Set up the menu, the user should select which option to run
    print("1) Read metadata")
    print("2) Export metadata")
    print("3) Delete metadata")
    print("4) Exit")
    print()
    print("[ * ] Select an option: ")
    option = input()
    return option

def parse_results(exif):
    for (k,v) in exif.items():
        if(("\x00") in str(v)):
            exif[k] = v.replace("\x00", "")
            if(exif[k] == ""):
                exif[k] = None
        if isinstance(v, bytes):
            try:
                exif[k] = v.decode()
            except:
                exif[k] = v
        if(k == "MakerNote") or (k == "UserComment") or (k == "PrintImageMatching"):
            try:
                value = v.decode()
                exif[k] = value.replace("\x00", "")
            except:
                exif[k] = " "   
    return exif

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


def traverse_folder(folder_path, action):
    if os.path.isdir(folder_path):
        print("[ PATH ] Looking for images in: " + folder_path)
        for file in os.listdir(folder_path):
            #If the file is a folder go inside it, recursively
            if os.path.isdir(os.path.join(folder_path, file)):
                traverse_folder(os.path.join(folder_path, file), action)
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                file_path = os.path.join(folder_path, file)
                if(action == "read"):
                    exif = read_metadata(file_path)
                    result = ("[ * ] Image found: " + file +"  ->  Path: "+ str(file_path) + '\n' + "[ ** ] Metadata: " + str(exif) + '\n')
                    print(result)
                if(action == "export"):
                    exif = read_metadata(file_path, export=True)
                    export_file = export_metadata(exif, file)
                    result = ("[ * ] Image found: " + file +"  ->  Path: "+ str(file_path) + '\n' + "[ ** ] Data exported into: " + str(export_file) + '\n')
                    print(result)
                if(action == "delete"):
                    delete_metadata(file_path)
                    result = ("[ * ] Image found: " + file +"  ->  Path: "+ str(file_path) + '\n' + "[ ** ] Metadata deleted: " + '\n')
                    print(result) 
    else:
        print("[ ERROR ] The folder does not exist!")



def read_metadata(file_path, export=False):
    image = Image.open(os.path.realpath(file_path))
    exifdata = image.getexif()
    if(len(exifdata)>0):
        exif = { ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS }
        exif = parse_results(exif)
        return exif
    else:
        exif = "No metadata found for this image"
        return exif

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

    
