""" 
Author: Ben Hogan

Description: This sript allows the user to choose a directory from which to clean out 
certain file types in batches. Answering n/no to any questions in the script 
will terminate the script.

1. Once the script has been run, it will prompt the user for a file path. 
Paste/type the absolute file path of the directory from which to remove 
files. 

2. Then the user will be given a summary of the file types that are present in 
that directory. 

3. From there the user will be asked if they would like to remove 
any file types from the directory. 

4. Upon ansering y/yes, the user may type (without ".") the extention type 
they wish to delete (directories not included). 

3. Then the user will be prompted to confirm and upon answering y/yes those 
file types will be deleted from the directory initially selected. 

4. The user will then be asked if they would like to remove any other files, 
upon which ansering y/yes would bring the user back to step 4.
"""

import os

file_type_profiles = []

def main():
    # 0. Promt for directory path to work with (Ubuntu example: /mnt/c/Users/John Doe/Deskop)
    path = input("\nEnter directory path you would like to work with: ")
    # 1. Read contents of directory for general stats (num of files, num of folders, file types present and how many, size of directory)
    try:
        filelist = os.listdir(path)
        print(f'\n   -->  {len(filelist)}  files/directories in {path}')
    except:
        print("File path does not exist")
        return

    # 2. Dict for each file type (type, num of files, memory, list of filenames or dir names), put each dict in a list
    for file in filelist:
        add_to_dict(file)
        
    # 3. Print dicts neatly
    print("\n    Directory Contents:")
    print("   --------------------")
    for type in file_type_profiles:
        if type['type'].upper() != 'DIRECTORIES':
            print("   {:>6}   {} Files".format(type['quantity'] ,type['type'].upper()))
        else: 
            print("   {:>6}   {}".format(type['quantity'], type['type'].upper()))

    # 4. Prompt for input on type to file delete, check input matches a type in the list of dicts
    if ensure_yes(input("\nDelete any of these file types? (y/n): ")):
        while True:
            type_to_delete = input("Type the extension the you'd like to delete (no '.' included): ")
            i = index_of(type_to_delete.lower())
            if i != None:
                # Are you sure?
                numOfFileType = file_type_profiles[i]['quantity']
                fileType = file_type_profiles[i]['type'].upper()

                if ensure_yes(input(f"""Are the user sure you want to delete all {numOfFileType} {fileType} files? (y/n): """)):
                    # Delete each filename in names list from directory
                    try:
                        for file in file_type_profiles[i]['names']: 
                            print(f'Removing --{file}--')
                            os.remove(os.path.join(path, file))
                    except:
                        print("\nAll of these types have either been deleted or moved")
                        pass
                    if not ensure_yes(input(f"\nWould you like to delete any other files? (y/n): ")): 
                        break
                else:
                    if not ensure_yes(input(f"\nWould you like to delete any other files? (y/n): ")): 
                        break
            else:
                print(f"\n{type_to_delete.upper()} file(s) not present in the {path}\n")
    else:
        print("No files were deleted")


def extension(filename):
    for rev_i in reversed(range(len(filename))):
        if filename[rev_i] == ".":
            return filename[(rev_i+1):]
    return filename


def index_of(ext):
    for i in range(len(file_type_profiles)):
        if file_type_profiles[i]['type'] == ext:
            return i
    return None


def add_to_dict(filename):
    '''Adds information to dictionary, if type is not present a dictionary is created'''
    filename = filename.lower()
    if "." in filename:
        type = extension(filename)
    else:
        type = 'directories'
    i = index_of(type)
    # if type present in list -> add qty, name
    if i != None:
        file_type_profiles[i]['quantity'] += 1
        file_type_profiles[i]['names'].append(filename)
    # else -> create Dictionary
    else:
        file_type_profiles.append({
            'type': type,
            'quantity': 1, 
            'names': [filename],
        })


def ensure_yes(response):
    response = response.lower()
    if response == 'y' or response == 'yes':
        return True
    elif response == 'n' or response == 'no':
        return False
    else:
        return


if __name__ == "__main__":
    main()
