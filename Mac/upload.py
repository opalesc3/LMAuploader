from internetarchive import upload
from internetarchive import search_items
from subprocess import call

# user required input
print("All fields marked with an * are required. Press enter to skip non-essential fields")
dir = str(input("Folder name*: "))
format = str(input("File format*: "))
date = str(input("Date*: "))
venue = str(input("Venue*: "))
coverage = str(input("Location*: "))
taper = str(input("Taper: "))
transferer = str(input("Transferer: "))
source = str(input("Source: "))
lineage = str(input("Lineage: "))

# generate other metadata
title = "Animal Collective Live at " + venue + " on " + date
year = date[:4]
id = "acollective" + date

# check if identifier is taken
search = search_items("identifier:" + id)
while len(search) > 0:
	suffix = str(input("Identifier [" + id + "] is taken, please add a suffix: "))
	id = id + suffix
	search = search_items("identifier:" + id)
print("Successfully generated identifier " + id + "!")

# call rename.sh [directory name] [date] [format] [id]
rename = str(input("Rename files? (y/n): "))
if rename == "y":
	call(["./rename.sh", dir, date, format, id])

# generate info file and description
descriptionHTML = ""
customDescription = input("Please enter a description (one line only).\n")
info = open(dir + "/" + id + "info.txt", "x")
info = open(dir + "/" + id + "info.txt", "w")
info.write("Animal Collective\n" + date + "\n" + venue + "\n" + coverage + "\n\n")
info.write(customDescription + "\n\n")
descriptionHTML = descriptionHTML + "<div>" + customDescription + "</div><div><br /></div>"

numSongs = int(input("\nSetlist length: "))
print("Paste setlist")
for i in range(numSongs):
	song = str(input())
	info.write(song + "\n")
	descriptionHTML = descriptionHTML + "<div>" + song + "</div>"

info.close()

# upload
md = {'mediatype': 'etree', 'collection': 'etree', 'collection': 'AnimalCollective', 'creator': 'Animal Collective', 'subject': 'Live concert', 'title': title, 'year': year, 'type': 'sound', 'venue': venue, 'date': date, 'coverage': coverage, 'description': descriptionHTML, 'taper': taper, 'transferer': transferer, 'source': source, 'lineage': lineage}

r = upload(id, dir + "/", metadata=md)
status = str(r[0].status_code)

if status == "200":
	print("Success!")
	print("https://archive.org/details/" + id)
else:
	print("Status code: " + status)
