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
	taggedTitle=$(ffprobe $file -show_entries format_tags=title -of compact=p=0:nk=1 -v 0)
	echo "Current tag: ${taggedTitle}"
	read -p "Track number: " num
	read -p "Track name: " name
	if [ ${#name} == 0 ]
	then
		name=$taggedTitle
	fi
	name=$(echo "${name}" | sed 's/ //g')
	newName="${id}t_${num}${name}${format}"
	read -p "Renaming to ${newName}"
	mv $file $folder/$newName
done
