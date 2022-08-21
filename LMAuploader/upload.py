from internetarchive import upload
from internetarchive import search_items
import music_tag
import datetime
import os
import requests
import lxml.html as lh

def main():
    bandAbbrDict = scrape()
    # user required input
    print("All fields marked with an * are required. Press enter to skip non-essential fields.")

    directory = emptyInputCheck("Folder name*: ")
    while(os.path.isdir(directory) is False):
        print("Invalid folder.")
        directory = str(input("Folder name*: "))

    bandName = emptyInputCheck("Band name*: ")
    bandAbbr = ""
    collection = ""
    nameValid = False
    while(nameValid is False):
        try:
            print("Fetching band abbreviation and collection name...")
            bandAbbr = bandAbbrDict[bandName]
            collection = collectionLookup(bandName)
            cont = input("Band abbreviation: " + bandAbbr + "\nCollection: " + collection + "\nDoes this information look correct? (y/n): ")
            if(cont == "y"):
                nameValid = True
            else:
                bandName = emptyInputCheck("Band name*: ")
        except Exception:
            bandName = emptyInputCheck("Invalid band name entered. Please check your spelling and remove special characters.\nBand name*: ")

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
    descFile = str(input("Description text file: "))
    while((os.path.isfile(descFile) is False or os.path.splitext(descFile)[-1].lower() != ".txt") and descFile != ""):
        print("Invalid file.")
        directory = str(input("Description text file: "))

    # generate other metadata
    title = bandName + " Live at " + venue + " on " + date
    year = date[:4]
    identifier = bandAbbr + date

    identifier = idCheck(identifier)
    print("Successfully generated identifier " + identifier + "!")

    re = str(input("Rename files? (y/n): "))
    if re == "y":
        rename(directory, identifier)

    description = genInfo(directory, bandName, identifier, date, venue, coverage, descFile)
    uploadFiles(directory, bandName, collection, identifier, title, date, year, venue, coverage, description, taper, transferer, source, lineage)


def scrape():
    url = "https://archive.org/audio/etree-band-abbrevs.php"
    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr = doc.xpath('//tr')
    dict = {}
    for i in range(2, len(tr)):
        dict[str(tr[i][0].text_content())] = str(tr[i][1].text_content()).split(";")[0]
    return dict


def collectionLookup(bandName):
    collection = ""
    for i in search_items('creator:"' + bandName + '" mediatype:collection'):
        collection = str(i['identifier'])
    return collection


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
        try:
            tags = music_tag.load_file(directory + "/" + filename)
        except Exception:
            continue
        else:
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
def genInfo(directory, bandName, identifier, date, venue, coverage, descFile):
    descriptionHTML = ""
    try:
        infoFile = open(str(directory) + "/" + str(identifier) + "info.txt", "x")
    except FileExistsError:
        pass
    infoFile = open(str(directory) + "/" + str(identifier) + "info.txt", "w")
    infoFile.write(bandName + "\n" + date + "\n" + venue + "\n" + coverage + "\n\n")

    if(descFile != ""):
        descList = genDescription(descFile)
        descriptionHTML = descriptionHTML + descList[0] + "<div><br /></div>"
        customDescription = descList[1]
    else:
        customDescription = input("Please enter a description (one line only).\n")
        descriptionHTML = descriptionHTML + "<div>" + customDescription + "</div><div><br /></div>"
    infoFile.write(customDescription + "\n\n")

    numSongs = int(emptyInputCheck("\nSetlist length: "))
    print("Paste setlist")
    for i in range(numSongs):
        song = emptyInputCheck()
        infoFile.write(song + "\n")
        descriptionHTML = descriptionHTML + "<div>" + song + "</div>"

    infoFile.close()
    return descriptionHTML


# read description from file and return with HTML tags
def genDescription(filename):
    descriptionHTML = ""
    description = ""
    file = open(filename, "r")
    for line in file:
        if(line == "\n"):
            line = "<br />"
        descriptionHTML = descriptionHTML + "<div>" + line.strip() + "</div>"
        description = description + line
    file.close()
    return [descriptionHTML, description]


# upload
def uploadFiles(directory, bandName, collection, identifier, title, date, year, venue, coverage, description, taper, transferer, source,
                lineage):
    print("Uploading...")
    md = {'mediatype': 'etree', 'collection': 'etree', 'collection': collection, 'creator': bandName,
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
