# /Users/4008575/Library/Python/3.8/bin/pytest
import re                       # regex
import sys                      # file manipulation
import glob                     # reading files in a folder
import json                     # json data
import shutil                   # copying template files
import fileinput                # file manipulation
import subprocess               # terraform and shell commands
from pprint import pprint       # json printing
from dictor import dictor       # jsonfile deserialization
from io_tools import io_tools as io
import sys

###
# to run:
# python3 program.py ../infra/ build_versions.json
###

###
# These vars need to go into a config file somewhere
###

# the directory to get the tf output from
terraform_directory = "/home/max/Desktop/repos/main_website/terraform"           

# cluster/env config file
terraform_values_template = "/home/max/Desktop/repos/main_website/terraform/configs/data.json"                                                            

versions_file_path = "/home/max/Desktop/repos/main_website/terraform/configs/build_versions.json"                                                                      # json file containing the desired provider/tf/module versions

# these need to go in a DB or a bucket
templates_dir = "/home/max/Desktop/repos/main_website/templates"           

# these need to go in a DB or a bucket
output_dir = "/home/max/Desktop/repos/main_website/terraform/output"                   

# todo: logging and tests
logs_dir = "/home/max/Desktop/repos/main_website/terraform/logs"                                                                                

# main program
def main():
    debug = False
    settings = {}
    vars = io.Variables(settings)
    vars.go_steppy = True
    vars.text_format = "json"
    vars.debug = True

    # copy template files from template_dir -> output_dir
    copy_templates(templates_dir, output_dir)

    # read versions.json into memory
    versions = io.read_file(versions_file_path, debug)
    vars.versions = json.loads(versions)

    # run terraform apply, then read the result of 'terraform output -json' into memory
    tf_init()

    #apply_terraform(target_dir, terraform_values_template, True)
    #tf_output = get_tf_output(target_dir, debug)

    # write terraform .tf files
    
    # write the versions.tf file
    #write_versions(versions, output_dir, debug)       
    
    # write all outputs from 'terraform output -json' to tfvars file
    #write_tfvars(tf_output, output_dir, variables)    
    
    # regex over all template files to populate variables
    #write_all(variables, versions, tf_output, debug)  

def copy_templates(templates_dir, output_dir):
    """"
    delete old output folder, copy templates to new output folder
    """
    shutil.rmtree('../output', ignore_errors=True)
    subprocess.run(['cp', '-r', templates_dir, output_dir])

def apply_terraform(target_dir, terraform_values_template, auto):
    """
    run a terraform apply from the target_dir with auto-approve y/n
    """
    terraform_raw = subprocess.run(
        ['terraform', 'apply', '-var-file=root_rg.tfvars', '-auto-approve'], cwd=terraform_directory, stderr=sys.stderr, stdout=sys.stdout, capture_output=True)
    print(terraform_raw.stdout)

def get_tf_output(target_dir, debug=False):
    """
    run 'terraform output -json' and capture the data and return it
    cwd changes working dir, newlines option removes "\n"s
    """
    terraform_raw = subprocess.run(
        ['terraform', 'output', '-json'], cwd=terraform_directory, capture_output=True, universal_newlines=True)

    try:
        terraform_values = json.loads(terraform_raw.stdout)
        print_pretty(terraform_values, debug)
    except:
        print(terraform_raw.stderr)

    return terraform_values

def tf_init():
    """
    Runs terraform init 
    """
    terraform_raw = subprocess.run(
        ['terraform', 'init', '-input=false', '-upgrade=true'], cwd=terraform_directory, stderr=sys.stderr, stdout=sys.stdout)
    print(terraform_raw.stdout)

def write_versions(versions, output_dir, debug):
    """
    messily constructs the versions.tf file
    """

    #write first line of versions file
    with open(output_dir + "/versions.tf", "a") as myfile:
        myfile.write("terraform {\n")

    # read the terraform version, write to output_dir/versions.tf
    tf_version = dictor(versions, "terraform.0.version")
    with open(output_dir + "/versions.tf", "a") as myfile:
        myfile.write("required_version = " + quote(tf_version) + "\n")

    # read provider data into memory
    providers = dictor(versions, "providers")

    ## assemble the HCL in memory
    with open(output_dir + "/versions.tf", "a") as myfile:
        myfile.write("required_providers {\n")

        # for each item in the provider json object:
        #       - get the name, version and source
        #       - if source = None, dont write the source filed to file
        for provider in providers:
            name = dictor(provider, "name")
            version = dictor(provider, "version")
            source = dictor(provider, "source")

            if source != "None":
                data_object = name + " = " + "{" + "\n" + "source = " + quote(source) + "\n" + "version = " + quote(version) + "\n}\n"
            else:
                data_object = name + " = " + "{" + "\n" + "version = " + quote(version) + "\n}\n"

            myfile.write(data_object)

    ## end providers, close the object
    with open(output_dir + "/versions.tf", "a") as myfile:
      myfile.write("}\n")

    #end terraform, close the object
    with open(output_dir + "/versions.tf", "a") as myfile:
      myfile.write("}\n")

    # super lazy formatting time
    subprocess.run(['terraform', 'fmt'], cwd=output_dir)

    modules = dictor(versions, "modules")
    for module in modules:
        name = dictor(module, "name")
        version = dictor(module, "version")
        source = dictor(module, "source")
        print_pretty("modules loaded", debug)

def quote(text):
    """
    returns a quoted variable
    """
    word = f'"{text}"'
    return word

def replace_in_file(old, new, path, debug=False): 
    """
    replaces a string inside target file
    """
    # regex function
    # takes <old_value> <new_value> <path/to/old_value>
    print_pretty(old + " --> " + new, debug)
    full_path = path
    with open(full_path, 'r+') as f:
        text = f.read()
        text = re.sub(old, new, text)
        f.seek(0)
        f.write(text)
        f.truncate()

def write_tfvars(terraform_values, output_dir, variables):
    """
    writes the variables.tf file
    """
    for section in terraform_values:
        values = dictor(terraform_values, "{}.value".format(section))

        if isinstance(values, str):
            values = dictor(terraform_values, "{}".format(section))
            for item in values:
                nested = dictor(values, "{}".format(item), pretty=True)
                name = section + "_" + item
                variables[name] = nested
        else:
            for item in values:
                nested = dictor(values, "{}".format(item), pretty=True)
                name = section + "_" + item
                variables[name] = nested

    #print_pretty(variables)
    dict_keys = list(variables.keys())
    dict_values = list(variables.values())
    count = 0
    for key in dict_keys:
        with open(output_dir + "/variables.tfvars", "a") as myfile:
            myfile.write(dict_keys[count] + " = " + dict_values[count] + "\n")
            count = count + 1

    # super lazy formatting time
    subprocess.run(['terraform', 'fmt'], cwd=output_dir)

def write_all(variables, versions, terraform_values, debug=False):   
    """
    regex over all template files to populate variables
    """
    # for each file in the output_dir,
    # - find any <UPPERCASE_VARIABLE_NAME>
    # - replace it with the value from global variables with the matching <lowercase_variable_name>

    for filepath in glob.iglob(output_dir+"/*"):
        print_pretty("modifying " + filepath, debug)
        keys = list(variables.keys())
        values = list(variables.values())
        count = 0
        for item in variables:
          replace_in_file(keys[count].upper(), values[count], filepath)
          count = count + 1

# runs the main program
main()
