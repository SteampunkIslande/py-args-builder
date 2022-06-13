#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import os
from jsonschema import ValidationError, validate
import json


def main(python_file: str, args_file: str):

    script_folder = os.path.dirname(os.path.realpath(__file__))

    env = dict()
    # Open json file that will define the arguments
    with open(args_file) as f:
        env = json.load(f)

    # Validate env using schema/args_schema.json as schema
    with open(os.path.join(script_folder, "schemas", "args_schema.json")) as f:
        schem = json.load(f)
        try:
            validate(instance=env, schema=schem)
        except ValidationError as e:
            print(str(e))
            return 1

    template_loader = FileSystemLoader(searchpath=script_folder)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template("args_template.py.jinja2")
    with open(python_file, "w") as f:
        f.write(template.render(**env))


if __name__ == "__main__":
    import argparse

    script_folder = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(
        description="Build argument parsing code in python"
    )
    parser.add_argument(
        "file",
        help="Python file to generate argument parser for (warning: will overwrite existing file)",
        dest="python_file",
    )
    parser.add_argument(
        "-a",
        "--arguments-file",
        help=f"Arguments definition to your program. See {os.path.join(script_folder,'schemas','args_schema')} for the schema",
        dest="args_file",
    )
    exit(main())
