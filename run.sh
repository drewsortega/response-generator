#!/bin/bash

# get directory of templates no matter CWD
script_path="$(dirname $(realpath $0))"
template_path="$script_path/templates"

# choose type of template
type="$(ls $template_path | rofi -dmenu -p "Choose type")"
template_path="$template_path/$type"
echo $template_path

# choose the template
template_filename="$(ls $template_path | rofi -dmenu -p "Choose template")"
template_path="$template_path/$template_filename"
echo $template_path

# run the template parser
template_text="$(python3 $script_path/parser.py $template_path)"

# type the template, letter-by-letter
echo "$template_text" | {
	IFS=read -r LINE;
	xdotool type -- "$LINE";
	
  	while IFS= read -r LINE; do
    		xdotool key Return;
    		xdotool type -- "$LINE";
  	done;
}
