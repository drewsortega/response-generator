#!/usr/bin/env python3

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import sys
import os
import jinja2
from rofi import Rofi

install_path = os.path.dirname(__file__)

# generate a Pango-formatted message to print in rofi
# to help users know what has been filled out, and what has not
def generate_vars_list(template_args, provided_args):
    filled_args = list()
    unfilled_args = list()
    message = ""

    # iterate listed required args, and determine
    # which have been not been provided.
    for arg in template_args:
        if arg not in provided_args:
            unfilled_args.append(arg)

    # if present, print the filled args and their values
    if len(provided_args) > 0:
        message = message + "<big>Filled Args:</big>\n"
        for arg_name, arg_val in provided_args.items():
            message = message + "  <b>{}:</b> {}".format(arg_name, arg_val)
        if len(unfilled_args) > 0:
            message = message + "\n\n"
    
    # if present, print the unfilled args and their values
    if len(unfilled_args) > 0:
        message = message + "<big>Unfilled Args:</big>\n"
        for arg in unfilled_args:
            message = message + "  <b>{}</b>\n".format(arg)

    # return complete message
    return message
        

# high-level template parser for importing if desired
def parse_template(template_path):
    # get the template data from the template file
    template_data = yaml.load(open(template_path), Loader=Loader)
    # get the global config info from the top-level global_vars.yml file
    global_data = yaml.load(open(os.path.join(install_path, 'global_vars.yml')), Loader=Loader)
    
    # create a template to parse the template_data and global_data into
    template = jinja2.Template(template_data['content'])

    # if there is an "args" object in template data, iterate it.
    if 'args' in template_data:
        args = dict()
        # create a rofi instance
        r = Rofi()

        # iterate args, request them, then add to args for templating
        for listed_arg in template_data['args']:
            entry = r.text_entry(listed_arg, message=generate_vars_list(template_data['args'], args))

            # if we cancelled the entry, return emptry string
            if entry == None:
                return ""

            # if we got a valid entry, continue
            args[listed_arg] = entry

    # combine args and global configurations into one object to pass
    template_fields = dict()
    template_fields['global'] = global_data
    template_fields['args'] = args

    # parse and return finished template
    return template.render(template_fields)

# if ran as main file, execute parse_template from args.
# note - no error handling is done here, as run.sh is expected
# to not error out here.
if __name__ == "__main__":
    # get template path from args
    template_path = sys.argv[1]

    # write new template to STDOUT
    print(parse_template(template_path))