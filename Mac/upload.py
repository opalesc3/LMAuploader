from internetarchive import upload
from internetarchive import search_items
from subprocess import call

# user required input
dir = str(input("Folder name: "))
format = str(input("File format: "))
date = str(input("Date: "))
venue = str(input("Venue: "))
coverage = str(input("Location: "))
taper = str(input("Taper: "))

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

# call rename.sh [directory name] [date] [format] [id]
rename = str(input("Rename files? (y/n): "))
if rename == "y":
	call(["./rename.sh", dir, date, format, id])

# generate info file and description
description = ""
info = open(dir + "/" + id + "info.txt", "x")
info = open(dir + "/" + id + "info.txt", "w")
info.write("Animal Collective\n" + date + "\n" + venue + "\n" + coverage + "\n\n")
info.write("Audio taken from the CollectedAnimals forum.\n\n")
description = description + "<div>Audio taken from the CollectedAnimals forum.</div><div><br /></div>"

numSongs = int(input("\nSetlist length: "))
print("Paste setlist")
for i in range(numSongs):
	song = str(input())
	info.write(song + "\n")
	description = description + "<div>" + song + "</div>"

info.write("\nUploaded in an effort to move all known Animal Collective live shows to the Live Music Archive.")
description = description + "<div><br /><div>Uploaded in an effort to move all known Animal Collective live shows to the Live Music Archive.</div>"

info.close()

# upload
md = {'mediatype': 'etree', 'collection': 'etree', 'collection': 'AnimalCollective', 'creator': 'Animal Collective', 'subject': 'Live concert', 'title': title, 'year': year, 'type': 'sound', 'venue': venue, 'date': date, 'coverage': coverage, 'description': description, 'taper': taper}

r = upload(id, dir + "/", metadata=md)
status = str(r[0].status_code)

if status == "200":
	print("Success!")
	print("https://archive.org/details/" + id)
else:
	print("Status code: " + status)