#/usr/bin/python3
# TODO: cleanup base libs
import json
from datetime import datetime
import sys
from deepdiff import DeepDiff
from dictor import dictor
# TODO: use me
import logging as log
from logging import debug
import os
import pandas as pd
import pathlib
from pyfiglet import Figlet
from pygments import highlight
from pygments.lexers.data import JsonLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers import get_lexer_by_name
from pygments.formatters import (Terminal256Formatter,
                                 HtmlFormatter,
                                 TerminalFormatter)
import re
import shutil
import time
import yaml
from yaml.loader import SafeLoader


# TODO: Logging
log_level = log.DEBUG
program_log = log.getLogger("my-logger")
#program_log.basicConfig(stream=sys.stderr, level=log_level)
program_log.info("logging config loaded")



def get_timestamp():
    """
    returns a timestamp in DD:MMM:YYYY (HH:MM:SS.f) format
    """

    now = datetime.now()
    timestamp = now.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    return timestamp


def get_epoch():
    """
    returns a timestamp in epoch format
    """

    # logging
    ts = get_timestamp()
    program_log.debug(f"function 'get_epoch' called at {ts}")

    timestamp = time.time()

    return timestamp


def read_file(path: str, debug, format: str = "json"):
    """
    reads json file from <path>: returns <json object>
    """

    # logging
    ts = get_timestamp()
    program_log.debug(f"function 'read_file' called at {ts}")

    # try to read the file
    message = print_pretty(f"trying to read: {path}", debug, format)
    program_log.debug(message)

    file_extension = pathlib.Path(path).suffix

    if file_extension == ".yaml":
        try:
            data = read_yaml_file(path)
            message = print_pretty(f"successfully read: {path}", debug, format)
            program_log.debug(message)

        except Exception:
            message = print_pretty(f"Failed to read: {path}", True)
            program_log.error(message)
            data = False

    if file_extension == ".json":
        try:
            data = read_json_file(path)
            message = print_pretty(f"successfully read: {path}", debug, format)
            program_log.debug(message)

        except Exception:
            message = print_pretty(f"Failed to read: {path}", True)
            program_log.error(message)
            data = False

    confirmed_data = validate_json_object(data)
    return confirmed_data['path']


def read_yaml_file(yaml_file_path):
    with open(yaml_file_path, 'r') as f:
        raw = f.read()
        yaml_object = yaml.safe_load(raw)

    return yaml_object


def read_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        raw = f.read()
        json_object = json.loads(raw)

    return json_object


def json_to_yaml(json_data, debug):
    """
    converts json_data: str into a json object{}
    converts the json object{} into a yaml: str
    """
    dumped = yaml.safe_dump(json.loads(json_data),
                            default_style="",
                            default_flow_style=False)
    return dumped


def yaml_to_json(yaml_file):
    """
    converts a yaml string into an object
    dumps the object as json
    """
    with open(yaml_file, 'r') as f:
      raw = f.read()
      yaml_object = yaml.safe_load(raw)
      json_data = json.dumps(yaml_object, indent=4, sort_keys=True)

    return json_data


def json_to_csv(json_file_path):
    """
    dump a json object to a file, then convert the file to a csv
    """
    with open(json_file_path, encoding='utf-8-sig') as f_input:
        df = pd.read_json(f_input)
        df.to_csv('test.csv', encoding='utf-8', index=False)


def print_pretty(data, debug: bool = False, format: str = "json"):
    """
    prettified json console output: returns <string>
    Generate JSON
    """
    json_data = {}
    try:
        json_data = validate_json_object(data)
    except:
        try:
            json_data = validate_json_file(data)
        except:
            if debug:
                name = input("Any key to continue")

    if json_data['readable'] != False:
        try:
            if format == "yaml":
                raw = json_to_yaml(data, debug)
                colorize_yaml(raw, debug)
            else:
                if format == "json":
                    colorize_json(json_data['path'], debug)
        except:
            print(f"Well shit, i cant parse this: {json_data}")
            if debug:
                name = input("Any key to continue")


def colorize_json(json_data, debug):
    """
    print colorful json data
    """

    # dump json to a string
    data = json.dumps(json.loads(json_data),
                        indent=" ",
                        separators=(',',': '),
                        sort_keys=True,
                        skipkeys=False)


    # create the highlighted text
    colorful = highlight(
        data,
        lexer=get_lexer_by_name("json"),
        formatter=Terminal256Formatter(style="fruity", linenos=True),
    )

    # print the highlighted text
    if debug == True:
        print(colorful)
    else:
        log = {}
        log['time'] = get_timestamp()
        log['data'] = colorful
        (log, True)


def colorize_yaml(data, debug):
    """
    prints colorful yaml data
    """

    # create highlighted text
    colorful = highlight(
        data,
        lexer=get_lexer_by_name("yaml"),
        formatter=Terminal256Formatter(style="fruity", linenos=True),
    )

    # print the highlighted text
    if debug == True:
        print(colorful)
    else:
        log = {}
        log['time'] = get_timestamp()
        log['data'] = colorful
        (log, True)


def validate_json_file(path: str, debug=False, format="json"):
    """
    takes a <file_path>, returns query{dict(<string>,<string>)}
    """
    message = f"json validation requested for : {path} "
    program_log.debug(message)

    query = {}
    query['path'] = path
    if read_file(path, debug) == False:
        query['readable'] = False
    else:
        query['readable'] = True
        message = f"Validation success : {path} was readable json"
        program_log.error(message)

    return query


def validate_json_object(object):
    """
    takes a jsonObject, returns query{dict(<string>,<string>)}
    """
    query = {}
    try:
        # is it already json?
        is_json = json.loads(object)
        query['readable'] = True
        query['path'] = object
    except:
        try:
            # can I make it json?
            raw_json = json.dumps(object,
                                  separators=(',', ': '),
                                  sort_keys=True,
                                  skipkeys=True)

            message = f"Validation success : {object} was readable json"
            program_log.debug(message)

            query['readable'] = True
            query['path'] = raw_json
        except:
            # nope, not json :(
            message = f"Validation failure : {object} was not readable json"
            program_log.error(message)

            query['readable'] = False
            if debug:
                name = input("Any key to continue")

    return query


def write_file(path: str, payload: str, debug = False, format="json"):
    """
    attempt to save <payload> to disk at <path> as json file
    """
    # check if the file and path exist on the target system,
    # if not, create it. return an error if we fail
    if not os.path.isfile(path):
        try:
            print_pretty(f"trying to write file: {path}", debug, format)
            text = dictor(payload, pretty=True)
            with open(path, "w") as save_file:
                save_file.write(text)
        except:
            print_pretty(f"failed to save: {path}", debug, format)
            if debug:
               name = input("Any key to continue")
    else:
    # if the file DOES exist, pop up a warning that I'm about to delete it.
        try:
            # this creates a long string of 80 #'s to break up text
            divider = "#".center(79,"#")

            # warn the user
            print_pretty(divider, debug, format)
            print_pretty(f"# file already exists: {path}", debug, format)

            desc = ("# if you dont want to delete the contents of the " +
                    "file on write, use the update_file() function")
            print_pretty(desc, debug, format)

            print_pretty(f"# clearing file... {path}", debug, format)
            print_pretty(divider, debug, format)

            # actually delete the file
            os.remove(path)

            # now try the whole loop again
            write_file(path, payload, debug)
        except:
            print_pretty(f"failed to save: {path}", debug, format)
            if debug:
                name = input("Any key to continue")

    # validate that we can read the file we wrote
    validate_json_file(path, debug)


def update_file(path: str, payload: str, debug = False, format="json"):
    """
    update an existing file on disk
    """
    try:
        with open(path, "a") as save_file:
            save_file.write(payload)
            save_file.close()
    except:
        print_pretty("failed to update: " + path, debug, format)


def make_dir(path: str, clear: bool = False, debug: bool = False,
             format="json"):
    """
    makes/deletes directory
    """
    # if the directory does not exist, try to create it
    if not os.path.isdir(path):
        print_pretty(f'Directory is not present. Creating {path}', debug,
                     format)
        try:
            os.makedirs(path)
        except:
            print_pretty(f"Unable to create dir at {path}", debug, format)
            if debug:
                name = input("Any key to continue")
    else:
    # if the directory DOES exist, notify that we will be removing and
    # overwriting it
        if not clear:
            print_pretty(f'Directory is present, but we are deleting it anyway! {path}', debug, format)
            print_pretty('clearing...', debug, format)
        else:
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except:
                print_pretty(f"failed to clear directory: {path}", debug,
                             format)
                if debug:
                    name = input("Any key to continue")


def replace_in_file(old: str, new: str, path: str, debug: bool = False,
                    format="json"):
    """
    replaces a string inside target file
    regex function
    takes <old_value> <new_value> <path/to/old_value>
    """
    print_pretty(old + " --> " + new, debug, format)
    full_path = path
    with open(full_path, 'r+') as f:
        text = f.read()
        text = re.sub(old, new, text)
        f.seek(0)
        f.write(text)
        f.truncate()


def quote(text: str):
    """
    returns a quoted variable
    quotes a variable
    """
    word = f'"{text}"'
    return word


def get_environment_vars(identitfier: str, env_vars: dict, debug=True,
                         format="json"):
    """
    reads and sets environment vars + str to bool conversion
    all environment variables are just interpreted as strings.
    this means we have to make sure we convert variables
    like TRUE, True, true etc.. to booleans when we find them
    """

    # new set of env vars
    new_vars = {}

    # for each env var, KEY => key
    for var in env_vars.keys():
        try:
            lower = str(var).lower()
            name = re.sub(identitfier, "", lower)
            new_vars[name] = os.getenv(var)
        except KeyError:
            print_pretty(f"Please set the environment variable {var}", debug,
                         format)

    # handle boolean conversion since all env vars are strings
    for var in new_vars:
        try:
            if new_vars[var] in ['True', "true", "yes","Yes"]:
                new_vars[var] = True
            else:
                if new_vars[var] in ['False', "false", "no","No"]:
                    new_vars[var] = False
        except KeyError:
            print_pretty(f"Please set the environment variable {var}", debug)

    return new_vars


class Variables(object):
    """
    ephemeral, human readable, stateful, json/yaml memory cache

    based on:
    stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem,

    attemptes to recreate C# getter/setter with an event listener:
    docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/using-properties
    https://docs.microsoft.com/en-us/dotnet/standard/events/
    """

    def __init__(self, settings):
        """
        Create a new memory cache
        """
        for item in settings:
            self.change_value(item, settings[item])


    def __setattr__(self, key, value):
        """
        ########################
        Event entrypoint
        custom events go in here
        ########################
        """

        ##
        # Diff Values
        ##
        debug = True
        format = "json"
        self.diff_values(key, value, debug, format)

        ##
        # prompt for confirmation
        ##
        self.steppy()

        super(Variables, self).__setattr__(key, value)


    def change_value(self, key, value):
        """
        Changes the value of settings and logs the change using deepdiff
        alters the behaviro here as this will be the global entry point
        for manual action
        """
        debug = True
        format = "json"
        self.diff_values(key, value, debug, format)
        self.settings[key] = value


    def get_current_value(self, key, value, debug=False):
        """
        Returns the current value of a key. Utility function
        for diff_values
        """
        current_value = None

        for section in self.__dict__:
            if section == key:
                current_value = self.__dict__[section]

            for item in section:
                if item == key:
                    current_value = self.__dict__[section][item]

        # and finally, return
        return current_value


    def diff_values(self, key, value, debug=False, format="json"):
        """
        returns a diff between current and proposed state
        try to find the current value if it exists
        opitmization needed
        """
        current_value = self.get_current_value(key, value, debug)

        # actually do the diff
        try:
            diff_data = DeepDiff(current_value, value)
            data = diff_data.to_json(indent='\t',
                                     separators=(',', ': '),
                                     sort_keys=True,
                                     skipkeys=True)

            # construct the diff message
            text = f"Change Requested for Value: {key}"
            print_pretty(text, debug, format)
            print_pretty(data, debug, format)

        except:
            text = f"Unable to diff: {current_value}"
            print_pretty(text, debug, format)


    def steppy(self):
        """
        If a settings names "go_steppy" is found in self.settings and is True,
        execution of tasks will pause upon memory item changes.
        """
        if "go_steppy" in self.__dict__:
            if self.go_steppy:
                name = input('Any Key to Approve')

