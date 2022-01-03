#/usr/bin/env Python3
"""
Demo script to showcase the io_tools library and what it can do for you
"""

import io_tools as io
import sys
from pygments.styles import get_all_styles

# we make the assumption taht just about anything you will be doing has the option to
# export and import either json or yaml. Therefore, io_tools simply injests and holds
# your data as a JSON object. This makes it highly portable.

# Here is our memory represented as json
settings = {}

# lets initialize the object
vars = io.Variables(settings)

# Now assign some values
vars.go_steppy = True
vars.text_format = "json"
vars.debug = True

# Pretty print the cache
io.print_pretty(vars.__dict__, vars.debug, vars.text_format)

# inspect the cache size
print(f"{sys.getsizeof(vars)} bytes")

# save the cache to a file (serialize)
io.write_file('cache.json', vars.__dict__, vars.debug)

# delete
del vars

# load from file (deserialize)
settings = io.read_file('cache.json', True)

# you will see on your terminal that each time a value in the memory
# object is updated, we are notified of the change with
# pretty printed data

# we can change the format of the output by passing the
# "format=''" flag to the io.print_pretty class
io.print_pretty(settings, True, "yaml")


# show off some features

# We dont have to create our memory structure
# every time form scratch, we can load existing yaml and
# json to bootstrap the memory schema

# io_tools translates boring data into human readable output
# it supports the use of multiple styles.
# lets make a list of all the styles:
#styles = list(get_all_styles())
