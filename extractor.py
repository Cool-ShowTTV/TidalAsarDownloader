from requests import get
import zipfile, shutil, os

"""Hacky script m8"""

OUTPUT_DIR = "output"
BETA = False # If to download beta builds instead
URL = f"https://download.tidal.com/desktop/windows{'/beta' if BETA else ''}"

# region Functions
def get_versions()->list:
    """Returns a list of version file names

    Returns:
        list: A list of version file names
    """
    
    ### Tidal API Info
    #   API return information is in the format of:
    #   <hash> <version_file_name> <file_size>
    #   
    #   The "RELEASES" file also starts with a "U+FEFF" which is a Zero Width unicode,
    #   So if you are parsing this file for the hash to verify make sure to only get A-Z and 0-9 characters
    #   
    #   There are two types of versions,
    #   - full.nupkg: The full package, which contains the full .asar file we want
    #   - delta.nupkg: A smaller update package, which only contains a .diff/.bsdiff file, which isn't helpful for us
    ###
    response = get(f"{URL}/RELEASES")
    if response.status_code != 200:
        print("Failed to fetch versions, status code:", response.status_code)
        print("Feel free to try again later if it's down.")
        exit(1)

    versions = []
    for line in response.text.splitlines():
        if "full.nupkg" in line:
            version = line.split(" ")[1]
            versions.append(version)

    return versions

def download_file(url:str, dest:str):
    """Downloads a file from the URL to dest location

    Args:
        url (str): URL to the asset
        dest (str): File path to the output

    Raises:
        ValueError: Raised if either are set as None
    """
    if url is None or dest is None: raise ValueError("URL and destination must not be None")
    response = get(url)
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url}")

def clean_temp():
    """Removes and recreates the temp folder
    """
    shutil.rmtree("temp")
    os.makedirs("temp")

def extract_asar(nupkg_file:str):
    """Searches for and extracts the ASAR file from the nupkg

    Args:
        nupkg_file (str): The update nupkg containing an ASAR file

    Raises:
        FileNotFoundError: If the ASAR file isn't found
    """
    with zipfile.ZipFile(nupkg_file, 'r') as zip_ref:
        asar_files = [f for f in zip_ref.namelist() if f.endswith('.asar')]
        if not asar_files:
            raise FileNotFoundError("No .asar file found in the nupkg package.")
        asar_file = asar_files[0]
        zip_ref.extract(asar_file, "temp")
        
        version_id = nupkg_file.split('-')[1]
        final_path = f"{OUTPUT_DIR}/TIDAL-{version_id}.asar"
        try:
            os.rename(f"temp/{asar_file}", final_path)
        except FileExistsError:
            print(f"{final_path} already exists, skipping.")
        clean_temp()

def download_and_extract(versions:list):
    """Downloads and extracts all versions in the list

    Args:
        versions (list): A list of version file names to download and extract
        out_name (str): The file to output the ASAR to
    """
    for version in versions:
        file_url = f"{URL}/{version}"
        dest_path = f"{OUTPUT_DIR}/{version}"
        download_file(file_url, dest_path)
        extract_asar(dest_path)
        print(f"Downloaded Tidal version {version} to {dest_path}")
# endregion

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    if not os.path.exists("temp"): os.makedirs("temp")
    else: clean_temp()
    
    versions = get_versions()
    versions.reverse()

    print(" _______  ___   ______   _______  ___        ______   ___     ")
    print("|       ||   | |      | |   _   ||   |      |      | |   |    ")
    print("|_     _||   | |  _    ||  |_|  ||   |      |  _    ||   |    ")
    print("  |   |  |   | | | |   ||       ||   |      | | |   ||   |    ")
    print("  |   |  |   | | |_|   ||       ||   |___   | |_|   ||   |___ ")
    print("  |   |  |   | |       ||   _   ||       |  |       ||       |")
    print("  |___|  |___| |______| |__| |__||_______|  |______| |_______|")

    count = 1
    print()
    print("0 > All")
    for version in versions:
        version_id = version.split('-')[1]
        print(f"{count} > {version_id}")
        count += 1
    
    print()
    print("Enter the number of the version you want to download, or 0 to download all")
    input_str = input("> ")
    try:
        choice = int(input_str)
        if choice == 0:
            download_and_extract(versions)
        elif 1 <= choice <= len(versions):
            download_and_extract([versions[choice - 1]])
        else:
            print("Invalid choice, exiting.")
    except ValueError:
        print("Invalid input, exiting.")

    os.removedirs("temp")
    # I remove temp to clean up but not nupkg just in case you need it later
    # Feel free to add that if you care.
