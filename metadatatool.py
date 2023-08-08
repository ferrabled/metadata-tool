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

def export_metadata(exif, file_name):
    toolpath = os.path.dirname(__file__)
    csv_file = os.path.join(toolpath + ("\\metadata\\" + file_name + "_metadata.csv"))

    if os.path.isfile(csv_file):
        csv_file = os.path.join(toolpath + ("\\metadata\\" + file_name + "_2_metadata.csv"))

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, escapechar="\\", quoting=csv.QUOTE_ALL, lineterminator='\n')
        try:
            if(type(exif) == str): 
                writer.writerow([exif])
            else:
                for key, value in exif.items():
                    writer.writerow([str(key), str(value)])
        except:
            print("[ ERROR ] Error writing metadata to file")
            print("[ ERROR ] " + str(sys.exc_info()[0]))
            writer.writerow("Error obtaining metadata")
    return csv_file


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

    
