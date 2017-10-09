#!/bin/bash

output_name=$1
shift
for img in $@; do
  convert $img -resize 520x726! "${img}.resized"
done
i=1
while [[ $@ ]]; do
  first="${1}.resized"
  shift
  if [[ -z $@ ]]; then
    second=$first
  else
    second="${1}.resized"
  fi
  shift
  if [[ -z $@ ]]; then
    third=$second
  else
    third="${1}.resized"
  fi
  convert $first $second $third +append ${i}.temp_row.jpg
  temp_imgs="$temp_imgs $first $second $third ${i}.temp_row.jpg"
  i=$((i+1))
  shift
done

table_command="convert"
for j in $(seq 1 $((i-1))); do
  table_command="$table_command ${j}.temp_row.jpg"
done
table_command="$table_command -append $output_name"
$table_command
rm -rf $temp_imgs
