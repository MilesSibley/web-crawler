import os
import csv
import shutil


#Each website you crawl is a seperate project (folder)
def create_project_dir(directory):
    #If the project already exists, overwrite it only if the user confirms
    if os.path.exists(directory):
        while True:
            overwrite = input("Overwrite existing results [y/n]?")
            if overwrite in ['y', 'n']:
                break
        if overwrite == 'y':
            print('Overwriting project ' + directory)
            shutil.rmtree(directory)
            os.makedirs(directory)
        elif overwrite == 'n':
            print('Nothing done.')
            exit()    
    elif not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)

# Create queue and crawled files (if not created)
def create_data_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    paths = project_name + '/paths.csv'
    page_status = project_name + '/page-status.csv'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')
    if not os.path.isfile(paths):
        write_file(paths, '')
    if not os.path.isfile(page_status):
        write_file(page_status, '')

# Create a new file
def write_file(path,data):
    f = open(path,'w')
    f.write(data)
    f.close()

# Add data onto an existing file
def append_to_file(path, data):
    with open(path,'a') as file:
        file.write(data + '\n')

# Add data onto an existing file
def append_to_csv(path, data):
    with open(path, 'a') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(data)

# Delete the contents of a file
def delete_file_contents(path):
    with open(path,'w'):
        pass

# Read a file and convert each line to set items
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

# Iterate through a set, each item will be a new line in the file
def set_to_file(links, file):
    delete_file_contents(file)
    for link in links:
        append_to_file(file, link)

# Iterate through a set, each item will be a new row
def set_to_csv(links, file):
    for link in links:
        row = link.split(',')
        append_to_csv(file,row)
