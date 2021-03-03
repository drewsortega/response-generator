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

# high-level template parser for importing if desired
def parse_template(template_path):
    # get the template data from the template file
    template_data = yaml.load(open(template_path), Loader=Loader)
    # get the global config info from the top-level config.yml file
    config_data = yaml.load(open(os.path.join(os.path.dirname(__file__), 'config.yml')), Loader=Loader)
    
    # create a template to parse the template_data and config_data into
    template = jinja2.Template(template_data['content'])

    # if there is an "args" object in template data, iterate it.
    if 'args' in template_data:
        args = dict()
        # create a rofi instance
        r = Rofi()

        # iterate args, request them, then add to args for templating
        for listed_arg in template_data['args']:
            args[listed_arg] = r.text_entry(listed_arg)

    # combine args and global configurations into one object to pass
    template_fields = dict()
    template_fields['config'] = config_data
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