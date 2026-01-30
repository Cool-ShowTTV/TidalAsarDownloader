# TidalAsarDownloader
A simple script to download all the ASAR updates on Tidal's server.

Might add support later to download asar for MAC too but if you know what you are doing it shouldn't be hard.

## What it does (if you care)
1. Sends a request to get all currently available versions from `https://download.tidal.com/desktop/windows/RELEASES`.
2. Extracts all `full.nupkg` file names from the list.
3. Downloads the Windows nupkg file to a temp folder.
4. Reads the nupkg as a zip copying the ASAR file from it.
5. Loops steps 2-4 for each nupkg file. 
