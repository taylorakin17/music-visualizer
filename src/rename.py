# iterate through a directory and rename all files in it
import os

def rename_files(path):
    """
    rename all files in a directory
    """
    file_list = os.listdir(path)
    for file_name in file_list:
        info = [] # symphony, movement

        # split the file name by spaces and periods
        file_name_split = file_name.split('_')
        for i in range(len(file_name_split)):
            # if the file name is a number, convert it to a string
            if file_name_split[i].isdigit():
                info.append(file_name_split[i])
            # if i == len(file_name_split) - 1:
            #     info.append(file_name_split[i][0])
        # rename the file
        if len(info) > 1:
            os.rename(path + file_name, path + "Concerto " +info[0] + " Mvt " + info[1] + '.mid')

if __name__ == '__main__':
    path = 'Mozart/'
    rename_files(path)