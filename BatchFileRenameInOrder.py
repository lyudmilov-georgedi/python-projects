import os
from tqdm import tqdm # import tqdm for the progress bar

directory = r"C:\xxx" # specify the directory containing the files
prefix = "ID_" # specify the prefix for the new file names

# get a list of all files in the directory
files = os.listdir(directory)

# sort the list of files by their names
files.sort()

# initialize the progress bar
pbar = tqdm(total=len(files))

# loop through the sorted list of files and rename them in numerical order
for i, file in enumerate(files):
    ext = os.path.splitext(file)[1] # get the file extension
    new_name = "{}{:04d}{}".format(prefix, i+1, ext) # create the new file name
    os.rename(os.path.join(directory, file), os.path.join(directory, new_name)) # rename the file
    pbar.update(1) # update the progress bar

# close the progress bar
pbar.close()
