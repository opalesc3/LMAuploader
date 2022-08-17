#!/usr/bin/env bash

folder="$1"
date="$2"
format="$3"
id="$4"

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

for file in ${folder}/*${format}
do
	echo -e "\n${file}"
	echo -n "Current tag: "
	ffprobe $file -show_entries format_tags=title -of compact=p=0:nk=1 -v 0
	read -p "Track number: " num
	read -p "Track name: " name
	name=$(echo "${name}" | sed 's/ //g')
	newName="${id}t_${num}${name}${format}"
	read -p "Renaming to ${newName}"
	mv $file $folder/$newName
done
