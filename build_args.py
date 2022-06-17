#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import os
from jsonschema import ValidationError, validate
import json
import typing


def overwrite_file(destfile: typing.TextIO, code: str):
    # Start overwriting with code
    destfile.write("# Begin generated code\n")

    for destline in code.split("\n"):
        destfile.write(destline + "\n")

    # End overwriting with code
    destfile.write("# End generated code\n")


def write_or_replace(code: str, sourcefile: typing.TextIO, destfile: typing.TextIO) -> None:
    """This function replaces blocks between
    '# Begin generated code' and '# End generated code'
    by string code, from file sourcefile to destfile.

    Args:
        code (str): Code to replace the block with
        sourcefile (typing.TextIO): A file opened for reading, containing original code
        destfile (typing.TextIO): A file opened for writing, to write source to (except for replaced block)
    """
    assert sourcefile.readable(), "Cannot read file"
    assert destfile.writable(), "Cannot write to file"
    overwrite = False
    overwrote = False
    for source_line in sourcefile:

        # Switch to overwriting if we see a block of generated code, and we haven't overwritten it yet
        if source_line.startswith("# Begin generated code") and not overwrote:
            overwrite = True
            overwrite_file(destfile, code)
            overwrote = True

        if source_line.startswith("# End generated code"):
            overwrite = False
            # Skip this line, we already wrote it with overwrite_file function
            continue

        if not overwrite:
            destfile.write(source_line)

    # We just rewrote the entire source file without overwriting, must to it now
    if not overwrote:
        overwrite_file(destfile, code)
        overwrote = True


def main(destfile: str, args_file: str):

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

    code = template.render(**env)

    if os.path.isfile(destfile):
        sourcefile = destfile + ".bak"
        os.rename(destfile, sourcefile)

        try:

            with open(sourcefile, "r") as backup_f:
                with open(destfile, "w") as new_f:
                    write_or_replace(code, backup_f, new_f)

        except FileNotFoundError as e:
            print(str(e))
            return 1

    return 0


if __name__ == "__main__":
    import argparse

    script_folder = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser(description="Build argument parsing code in python")
    parser.add_argument(
        "destfile",
        help="Python file to generate argument parser for (warning: will overwrite existing file)",
    )
    parser.add_argument(
        "-a",
        "--arguments-file",
        help=f"Arguments definition to your program. See {os.path.join(script_folder,'schemas','args_schema')} for the schema",
        dest="args_file",
        required=True,
    )
    args = vars(parser.parse_args())
    exit(main(**args))
