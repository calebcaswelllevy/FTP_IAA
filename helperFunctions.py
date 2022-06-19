
import os
from astropy.io import fits

#Define helper functions to get matching files and then access them on the local machine:

def get_file_names(ftp: object, folder: str, target: str = '.+-(vis|nir)_[AB].fits$'):
    '''
    Returns a list of file names matching the target regex string

    PARAMETERS:
    :ftp::
    :folder: string path to the target directory:
    :target: string regex pattern to search for. Files matching the pattern will be appended and returned:

    RETURNS:
    :files: list of strings of file pathways:
    '''
    files = []
    data = []
    try:
        ftp.cwd(folder)
        ftp.dir(data.append)
    except:
        print(f"ERROR: could not connect to directory: {folder}")

    for file_name in data:
        if re.search(target, file_name):
            files.append(file_name)

    return files


def retrieve(ftp: object, files: list, target_directory: str = "./retrieved_fits_files/",
             erase_previous_files: bool = False):
    '''
    wrapper function that downloads files in the supplied list.

    PARAMETERS:
    :ftp: an ftp connection over which to access files:
    :files: list of strings containing the :
    :erase_previous_files: boolean determining to erase prior files in the target directory, if it exists:

    RETURNS: None

    '''

    # test if target dir exists:
    directory_exists = os.path.isdir(target_directory)
    # if not, create it:
    if not directory_exists:
        os.mkdir(target_directory)
    elif erase_previous_files:  # clear contents of target directory
        prior_files = os.listdir(target_directory)
        [os.remove(file) for file in prior_files]

    #acess each of the files and download them to the target_directory
    for file in files:
        try:
            get_file_from_ftp(ftp, file, target_directory)
        except:
            print(f"ERROR: could not access file: {file}")


def get_file_from_ftp(ftp: object, file_name: str, target_directory: str):
    '''
    Downloads local copy of file over ftp.

    PARAMETERS:
    :ftp: an ftp connection object:
    :file_name: string location of file to download:

    RETURNS: None
    '''
    # TODO
    # download local copy
    with open(target_directory + file_name, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftp.retrbinary(f"RETR {file_name}", file.write)


def extract_data_from_fits_header(file: str, variable_keyword: str, pathway = "./retrieved_fits_files/") -> str:
    '''
    Returns the value of the variable keyword from the fits header.

    PARAMETERS:
    :file: the pathway to the fits file:
    :variable_keyword: The keyword in corresponding to the desired variable in the header:
    :pathway: str pathway to directory containing the file:

    RETURNS:
    :variable: the desired variable's value:
    '''
    file = pathway + file

    try:
        header = fits.getheader(file)
    except:
        return f'Error: could not access {file}'
    try:
        variable = header[variable_keyword]
        return variable
    except:
        return None
        print(f'Error: {variable_keyword} could not be found in {file}')



