from PIL import Image, ExifTags
import sys
import os
import csv

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



def delete_metadata(file_path):
    # Delete metadata from a file
    image = Image.open(os.path.realpath(file_path))
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    # Save the image without metadata
    image_without_exif.save(os.path.realpath(file_path))



art = """    __  ___     __            __      __           ______            __
   /  |/  /__  / /_____ _____/ /___ _/ /_____ _   /_  __/___  ____  / /
  / /|_/ / _ \/ __/ __ `/ __  / __ `/ __/ __ `/    / / / __ \/ __ \/ / 
 / /  / /  __/ /_/ /_/ / /_/ / /_/ / /_/ /_/ /    / / / /_/ / /_/ / /  
/_/  /_/\___/\__/\__,_/\__,_/\__,_/\__/\__,_/    /_/  \____/\____/_/   
                                                                       """


def main():
    print(art)
    # Main function
    # Set up the menu
    option = init_menu()
    # Check the option selected by the user
    print("[ ^ ] Select the file or folder to delete the metadata: ")
    file_path = input()
    if option == "1":
        # Read metadata
        traverse_folder(file_path, 'read')
    elif option == "2":
        # Export metadata
        traverse_folder(file_path, 'export')
    elif option == "3":
        # Delete metadata
        traverse_folder(file_path, 'delete')
    elif option == "4":
        # Exit
        print("[ x ] Exiting")
        sys.exit()
    else:
        print("[ x ] Invalid option, exiting")
        sys.exit()

    
if __name__ == "__main__":
    main()

    
