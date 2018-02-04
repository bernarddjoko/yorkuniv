import requests
import os
import subprocess
import zipfile


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def getUrlFromString(source_string):
    lst = source_string.split(" ")
    # return the url for the file
    return lst[2]
    
def extractAllFiles(dir_path):
    total_files = 0 
    number_of_files_unzipped = 0 
    for path, dir_list, file_list in os.walk(dir_path):
        
        for file_name in file_list:
            total_files = total_files + 1
            print(file_name)
            file_name = file_name.strip()
            if file_name.endswith(".zip"):
               
                path = os.path.abspath(path)
                abs_file_path = os.path.join(path, file_name)
                print("unzipping: " + abs_file_path)
                
                # The following three lines of code are only useful if 
                # a. the zip file is to unzipped in it's parent folder and 
                # b. inside the folder of the same name as the file
                
                parent_path = os.path.split(abs_file_path)[0]
                output_folder_name = os.path.splitext(abs_file_path)[0]
                output_path = os.path.join(parent_path, "data")
                try:
                    zip_obj = zipfile.ZipFile(abs_file_path, 'r')
                    print(abs_file_path)
                    print("outputpath: " + output_path)
                    zip_obj.extractall(output_path)
                    zip_obj.close()
                    number_of_files_unzipped = number_of_files_unzipped + 1
                except zipfile.BadZipFile as exc:
                    print(exc)
                    
    #print("total_files: " +  str(total_files))
    print("number_of_files_unzipped: " + str(number_of_files_unzipped))            
                
                

def fetchFile(url,target_path):
    # master_url = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
    # target_path = "master.txt"
    url = url.strip()
    target_path = target_path.strip()
    print(target_path)
    print(url)
    
    response = requests.get(url, stream=True)
    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
           handle.write(chunk)
    

def downloadZipFiles(path_file,data_type, number_of_files_to_download=3000):
    ## lets fetch the files in each list 
    count = 0
    with open(path_file, 'r') as infile:
            for path in infile:
                 if count >= number_of_files_to_download: 
                     break
                 else:
                     path = getUrlFromString(path)
                     output_path = path.split("/")[4]
                     fetchFile(path,data_type+'/' + output_path)
                     print("number_of_files_to_download " + str(number_of_files_to_download))
                     print("count " + str(count))
                     count = count + 1   
              

createFolder("events")
createFolder("mentions")
createFolder("events/data")
createFolder("mentions/data")

# get the master file 
master_url = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt'
master_file_path = "master.txt"
fetchFile(master_url,master_file_path)


eventfile = open("events/events.txt", 'w')
mentionsfile = open("mentions/mentions.txt", 'w')

with open(master_file_path, 'r') as infile:
        for line in infile:
            if "export" in line:
               eventfile.write(line)
            if "mentions" in line:
                mentionsfile.write(line)


# should run these is parallel
path = os.path.abspath("mentions")
path = os.path.join(path, "mentions.txt")
data_type = "mentions"
downloadZipFiles(path,data_type)

path = os.path.abspath("events")
path = os.path.join(path, "events.txt")
data_type = "events"
downloadZipFiles(path,data_type)

extractAllFiles("mentions")
extractAllFiles("events")

                     