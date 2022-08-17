# ancoLMAuploader
Scripts to help upload Animal Collective bootlegs to the Live Music Archive on the Internet Archive
# Requirements
- The Mac Terminal application (currently only works on Mac).
- The latest version of python. Please consult the internet for this, it can be finicky to set up.
- The internetarchive library. Instructions for installation can be found [here](https://archive.org/services/docs/api/internetarchive/installation.html).
- Your archive.org credentials in a config file. This can be done by running `ia configure` and entering your email and password.
- A folder of the music files you are trying to upload to LMA, placed in the same folder as the two scripts. Use `chmod 700 rename.sh` to make the bash script executable. 
# What these scripts do
The `rename.sh` script is a helper bash script that allows you to rename files to fit the LMA specifications. It takes four arguments: the name of the folder containing the music files, the date in yyyy-mm-dd format, the format of the files with a period in front (for example `.mp3`), and the identifier (in the format `acollectiveyyyy-mm-dd`). The python script calls on this one, but to run the script by itself you would enter the following:
```
./rename.sh [folder name] [yyyy-mm-dd] [file format] [identifier]
```
For each file it prints the current name, the "title" tag embeded in the file, and allows the user to input the track number and track name. If there is more than one song in a file please separate the names with a dash (-). It then prints what the file will be renamed to. Press `enter` after to continue to the next file. Please consult the [CollectedAnimals Live Recordings topic](https://collectedanimals.org/viewtopic.php?f=14&t=41) while doing this as the files downloaded from there may not be in order or have the correct track numbers/names.

Exerpt of the `rename.sh` script in progress:
```
Animal Collective - 2004-05-06, Electricity Showroom, London/01 Banshee Beat _ Kids on Holiday.mp3
Current tag: Banshee Beat / Kids on Holiday
Track number: 01
Track name: Banshee Beat - Kids On Holiday
Renaming to acollective2004-05-06t_01BansheeBeat-KidsOnHoliday.mp3
```

The `upload.py` script allows the user to input the information required to upload a bootleg to LMA, generates an info file, and gives the option to rename the files using the `rename.sh` script. Run the script using `python upload.py` while in the same folder as the two scripts and the folder of music files to upload. The script will prompt you for the required information. When it comes to enter the setlist, first enter the total number of entries when prompted, then paste the entire setlist after the next prompt. If successful, the script will notify the user and print the link of the archive.org entry. 

The generated description for these will always be of the same format.
```
Audio taken from the CollectedAnimals forum.

[setlist]

Uploaded in an effort to move all known Animal Collective live shows to the Live Music Archive.
```
# What these scripts do not do
These scripts have no input validation, so please take care while entering information. Please also ensure that all the files you are uploading are of the same format. Do not try to use these scripts on singular unsplit bootlegs or videos. These scripts also do not affect the tags of the music files. To edit those please use separate software. 

These scripts were written to upload Animal Collective bootlegs only, though they may be one day updated to be able to upload things to LMA for any band.
# Bugs
If you encounter bugs or errors please report an issue or if you are on the Collection of Animals server, take a screenshot and describe the issue on Discord. Thank you!
# TODO
- Allow for custom description through separate text file.
- Allow for more fields (transferred by, source, lineage).
- Input validation.
- Better check for usable identifier.
- Remove need for `rename.sh` by writing it in python.
- Create version that works on Windows.
