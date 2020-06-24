import argparse

parser = argparse.ArgumentParser(
    description='Process some integers.',
    # usage='usage of args default generated'
)
parser.add_argument(
    'file',  # Either a name or a list of option strings, this will be without -
    '-f', '--file',  # Either a name or a list of option strings, this will be with - --
    metavar='file',  # A name for the argument in usage messages.
    nargs=0,  # The number of command-line arguments that should be consumed.
              # Can be 1,2,3,0 or '+*?', this return array if value is number (also if number is 1)
    type=str,  # The type to which the command-line argument should be converted. str, int, open
    default='',  # The value produced if the argument is absent from the command line.
    required=True,  # Whether or not the command-line option may be omitted (optionals only).
    action='store_const', const='const',  # Store constant to the parameter
    # action='store_false',  # Store True to the parameter if is written
    # action='store_true',  # Store False to the parameter if is written
    # action='append',  # This stores a list, and appends each argument value to the list
    choices=['rock', 'paper', 'scissors'],  # A container of the allowable values for the argument.
    help='searching file, word'
)
parser.add_argument(
    '-r', '--end-regex',
    action='store_true',
)

args = parser.parse_args()
print(args.file)
print(args.end_regex)
