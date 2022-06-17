def dream():
    pass


def contemplate():
    pass


# Begin generated code


import argparse


def main():

    parser = argparse.ArgumentParser(description="Some description")

    sub_parser = parser.add_subparsers(dest="subparser")
    # Arguments to this parser will be common to every subcommand, and available as members of args.
    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument(
        "-l", "--loss", help="Some help", type=str, default="BCELoss", choices=("BCELoss", "L1Loss")
    )

    # This is one subcommand parser, with its very own arguments. These will be available as member of args
    contemplate_parser = sub_parser.add_parser("contemplate", parents=[parent_parser])

    contemplate_parser.add_argument(
        "-i",
        "dataset_dir",
        help="Path to folder where every child folder is one label",
        type=str,
        default=images,
    )

    contemplate_parser.set_defaults(func=contemplate)

    # This is one subcommand parser, with its very own arguments. These will be available as member of args
    dream_parser = sub_parser.add_parser("dream", parents=[parent_parser])

    dream_parser.add_argument(
        "-i",
        "--input",
        help="Image to use as input. Defaults to images",
        type=str,
        default=images,
    )

    dream_parser.set_defaults(func=dream)

    args = vars(parser.parse_args())
    func = args["func"]

    chosen_scenario = args["subparser"]
    del args["subparser"]

    del args["func"]

    return func(**args)


if __name__ == "__main__":
    exit(main())
# End generated code
