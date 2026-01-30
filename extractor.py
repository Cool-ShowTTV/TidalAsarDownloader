from requests import get
import zipfile, shutil, os

"""Hacky script m8"""

OUTPUT_DIR = "output"

# region Functions
def get_versions():
    response = get("https://download.tidal.com/desktop/windows/RELEASES")
    if response.status_code != 200: exit(1)

    versions = []
    for line in response.text.splitlines():
        if "full.nupkg" in line:
            version = line.split(" ")[1]
            versions.append(version)

    return versions

def download_file(url, dest):
    if url is None or dest is None: raise ValueError("URL and destination must not be None")
    response = get(url)
    if response.status_code == 200:
        with open(dest, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download {url}")

def clean_temp():
    shutil.rmtree("temp")
    os.makedirs("temp")

def extract_asar(nupkg_file, out_name):
    with zipfile.ZipFile(nupkg_file, 'r') as zip_ref:
        asar_files = [f for f in zip_ref.namelist() if f.endswith('.asar')]
        if not asar_files:
            raise FileNotFoundError("No .asar file found in the nupkg package.")
        asar_file = asar_files[0]
        zip_ref.extract(asar_file, "temp")
        
        version_id = nupkg_file.split('-')[1]
        final_path = f"{out_name}/{version_id} asar.asar"
        try:
            os.rename(f"temp/{asar_file}", final_path)
        except FileExistsError:
            print(f"{final_path} already exists, skipping.")
        clean_temp()
# endregion

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    if not os.path.exists("temp"): os.makedirs("temp")
    else: clean_temp()
    
    versions = get_versions()
    for version in versions:
        file_url = f"https://download.tidal.com/desktop/windows/{version}"
        dest_path = f"{OUTPUT_DIR}/{version}"
        download_file(file_url, dest_path)
        extract_asar(dest_path, OUTPUT_DIR)
        print(f"Downloaded Tidal version {version} to {dest_path}")

    os.removedirs("temp")
    # I remove temp to clean up but not nupkg just in case you need it later
    # Feel free to add that if you care.
