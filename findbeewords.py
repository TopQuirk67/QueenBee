import argparse
import csv
import os
import glob

# Get a list of all csv files in the directory
files = glob.glob('/Users/garethhouk/Documents/play/QueenBee/data/*.csv')

# Find the most recent file
latest_file = max(files, key=os.path.getctime)

# Create the parser
parser = argparse.ArgumentParser(description="Process a seven-letter string.")

# Add the argument
parser.add_argument('--letters', type=str, help='a seven-letter string')
parser.add_argument('--word', type=str, help='a word to search for')

# Parse the arguments
args = parser.parse_args()

# Check if both letters and word arguments are provided
if args.letters and args.word:
    raise argparse.ArgumentTypeError("Only one of --letters or --word should be provided")

# Check if the input is a seven-letter string
if args.letters and len(args.letters) != 7:
    raise argparse.ArgumentTypeError("Input should be a seven-letter string")

if args.letters:
    input_letters = ''.join(sorted(args.letters)).upper()
    print(f"Searching for {input_letters} in {latest_file}")
elif args.word:
    input_word = args.word.upper()
    print(f"Searching for {args.word} in {latest_file}")

# Open the CSV file
with open(latest_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # Search the CSV database
        date, letters, words = row
        # print(''.join(sorted(args.letters)), letters)
        if args.letters:
            if input_letters == ''.join(sorted(letters)):
                print(f"Found {args.letters} in database {date} {letters}")
        elif args.word:
            if letters[0] in input_word and set(input_word).issubset(set(letters)):
                print(f"{input_word} could have been an answer on {date} {letters}")
            if input_word in words:
                print(f"Found {args.word} in database {date} {letters}")
