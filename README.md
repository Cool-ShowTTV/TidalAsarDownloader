# TidalAsarDownloader
A simple script to download all the ASAR updates on Tidal's server. This is useful for debuging something that worked in the last version in custom clients.

## What it does (if you care)
1. Sends a request to get all currently available versions from `https://download.tidal.com/desktop/windows/RELEASES`.
2. Extracts all `full.nupkg` file names from the list.
3. Downloads the Windows nupkg file to a temp folder.
4. Reads the nupkg as a zip copying the ASAR file from it.
5. Loops steps 2-4 for each nupkg file. 

## Screenshot
<img width="743" height="442" alt="image" src="https://github.com/user-attachments/assets/6b6799bc-6833-4b78-9b86-cf65464d26dd" />
