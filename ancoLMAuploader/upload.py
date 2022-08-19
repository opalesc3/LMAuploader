from internetarchive import upload
from internetarchive import search_items
import music_tag
import datetime
import os

def main():
    # user required input
    print("All fields marked with an * are required. Press enter to skip non-essential fields.")

    directory = emptyInputCheck("Folder name*: ")
    while(os.path.isdir(directory) is False):
        print("Invalid folder.")
        directory = str(input("Folder name*: "))

    date = emptyInputCheck("Date*: ")
    dateValid = False
    while(dateValid is False):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            dateValid = True
        except ValueError:
            print("Invalid date. Please enter in yyyy-mm-dd format.")
            date = emptyInputCheck("Date*: ")

    venue = emptyInputCheck("Venue*: ")
    coverage = str(input("Location: "))
    taper = str(input("Taper: "))
    transferer = str(input("Transferer: "))
    source = str(input("Source: "))
    lineage = str(input("Lineage: "))

    # generate other metadata
    title = "Animal Collective Live at " + venue + " on " + date
    year = date[:4]
    identifier = "acollective" + date

    identifier = idCheck(identifier)
    print("Successfully generated identifier " + identifier + "!")

    re = str(input("Rename files? (y/n): "))
    if re == "y":
        rename(directory, identifier)

    description = genInfo(directory, identifier, date, venue, coverage)
    uploadFiles(directory, identifier, title, date, year, venue, coverage, description, taper, transferer, source, lineage)


# check if identifier is taken
def idCheck(identifier):
    search = search_items("identifier:" + identifier)
    while len(search) > 0:
        suffix = emptyInputCheck("Identifier [" + identifier + "] is taken, please add a suffix: ")
        identifier = identifier + suffix
        search = search_items("identifier:" + identifier)
    return str(identifier)


# Rename files
def rename(directory, identifier):
    for file in os.listdir(directory):
        filename = str(os.fsdecode(file))
        print("\n" + filename)
        ext = os.path.splitext(file)[-1].lower()
        tags = music_tag.load_file(directory + "/" + filename)

        print("Current track number and track title: " + str(tags['tracknumber']).zfill(2) + " " + str(tags['title']))
        print("Leave blank to use current values.")
        num = str(input("Track number: "))
        while(num.isnumeric() is False and num != ""):
            print("Please enter digits only.")
            num = str(input("Track number: "))
        title = str(input("Track title: ")).replace(" ", "")
        if len(num) == 0:
            num = str(tags['tracknumber']).zfill(2)
        if len(title) == 0:
            title = str(tags['title']).replace(" ", "")
        title = "".join([i if i not in "\/:*?<>|" else "-" for i in title])
        newName = identifier + "t_" + num + title + ext
        input("Renaming file to " + newName)
        os.rename(directory + "/" + filename, directory + "/" + newName)


# generate info file and description
def genInfo(directory, identifier, date, venue, coverage):
    descriptionHTML = ""
    customDescription = input("Please enter a description (one line only).\n")
    infoFile = open(str(directory) + "/" + str(identifier) + "info.txt", "x")
    infoFile = open(str(directory) + "/" + str(identifier) + "info.txt", "w")
    infoFile.write("Animal Collective\n" + date + "\n" + venue + "\n" + coverage + "\n\n")
    infoFile.write(customDescription + "\n\n")
    descriptionHTML = descriptionHTML + "<div>" + customDescription + "</div><div><br /></div>"

    numSongs = int(emptyInputCheck("\nSetlist length: "))
    print("Paste setlist")
    for i in range(numSongs):
        song = emptyInputCheck()
        infoFile.write(song + "\n")
        descriptionHTML = descriptionHTML + "<div>" + song + "</div>"

    infoFile.close()
    return descriptionHTML


# upload
def uploadFiles(directory, identifier, title, date, year, venue, coverage, description, taper, transferer, source,
                lineage):
    md = {'mediatype': 'etree', 'collection': 'etree', 'collection': 'AnimalCollective', 'creator': 'Animal Collective',
          'subject': 'Live concert', 'title': title, 'year': year, 'type': 'sound', 'venue': venue, 'date': date,
          'coverage': coverage, 'description': description, 'taper': taper, 'transferer': transferer, 'source': source,
          'lineage': lineage}

    r = upload(identifier, directory + "/", metadata=md)
    status = str(r[0].status_code)

    if status == "200":
        print("Success!")
        print("https://archive.org/details/" + identifier)
    else:
        print("Status code: " + status)

def emptyInputCheck(prompt=""):
    i = str(input(prompt))
    while(len(i) == 0):
        print("This field cannot be left empty.")
        i = str(input(prompt))
    return i

if __name__ == "__main__":
    main()
