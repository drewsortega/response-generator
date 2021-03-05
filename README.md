# Rofi Response Generator
Generates responses based on a global variables and individual requests to generate responses and type them out, emulating keyboard output.

## Installation
1. Install required system packages
- xdotool
- rofi
- python3
- pip3
2. Install required python3 packages
```bash
pip3 install -r requirements.txt
```
3. Add any globally accessible vars you want to have for your templates to `global_vars.yml`

## Running
```bash
./run.sh
```

## Creating a new Template
1. Add a `[NAME].yml` file to a directory in `templates/` (or create a new one)
1. add a `content` field, with jinja2 template options. Note this only supports plain-fields at the moment, no lists.
    - for every newline you want in the template, you must pre-fix it with an extra newline. For example, for 1 newlines, write 2. For 2 newlines, write 3, etc.
    - for global variables from `global_vars.yml`, pre-face every item with `global.`. For example, `global.name`
    - for requested-variables each time you run a template, pre-face every item with `args.`. For example, `args.user_name`
1. If you used any `args.` objects, add an `args` list, with bulleted items for every arg you wish to request.

## Example Template File
```yml
content: "Hello {{ args.recipient_name }},


Thanks for you email.



Best,


{{ global.name }}

{{ global.role }}"
args:
    - recipient_name
```

# Example `global_vars.yml` File
```yml
name: John Doe
role: Systems Developer
```