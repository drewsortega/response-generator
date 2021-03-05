#!/bin/bash

function start_prompt {
	# get directory of templates no matter CWD
	script_path="$(dirname $(realpath $0))"
	template_path="$script_path/templates"

	# choose type of template
	type="$(ls $template_path | rofi -dmenu -p "Choose type")"

	# check to see if a type was specified. if no type, cancel.
	if [ -n "$type" ]; then
		template_path="$template_path/$type"

		# choose the template
		template_filename="$(ls $template_path | rofi -dmenu -p "Choose template")"

		# check to se if a template was chosen. If not, restart.
		if [ -n "$template_filename" ]; then
			template_path="$template_path/$template_filename"

			# run the template parser
			template_text="$(python3 $script_path/parser.py $template_path)"

			# check to see if there is a valid string here
			if [ -n "$template_text" ]; then
				# type the template, letter-by-letter
				echo "$template_text" | {
					IFS=read -r LINE;
					xdotool type -- "$LINE";
					
					while IFS= read -r LINE; do
							xdotool key Return;
							xdotool type -- "$LINE";
					done;
				}
			fi
		else
			# restart prompt
			start_prompt
		fi
	fi
}

# do initial run of program
start_prompt