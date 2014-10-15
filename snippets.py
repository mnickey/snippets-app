import logging
import csv
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="output.log", level=logging.DEBUG)

def put(name, snippet, filename):
	""" Store a snippet with an associated name in the CSV file """
	logging.info("Writing {!r}:{!r} to {!r}".format(name, snippet, filename))
	logging.debug("Opening file")
	with open(filename, "a") as f:
		writer = csv.writer(f)
		logging.debug("Writting snippet to file...")
		writer.writerow([name, snippet])
	logging.debug("Write Sucessful")
	return name, snippet

def get(name, snippet, filename):
	logging.info("Retreiving {!r}:{!r} to {!r}".format(name, snippet, filename))
	logging.debug("Opening and reading file")
	with open(filename, "r") as f:
		reader = csv.reader(f)
		logging.debug("Reading file for snippet")
		for row in reader:
			if row == snippet:
				print snippet
	return

def make_parser():
	""" Construct a command line parser """
	logging.info("Constructing parser")
	description = "Store and retrieve snippets of text"
	parser = argparse.ArgumentParser(description=description)

	subparsers = parser.add_subparsers(dest= "command", help="Available commands")

	# Subparser for the put command
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help="Store a snippet")
	put_parser.add_argument("name", help="The name of the snippet")
	put_parser.add_argument("snippet", help="The snippet text")
	put_parser.add_argument("filename", default="snippets.csv", nargs="?",
                            help="The snippet filename")

	logging.debug("Constructing get parser")
	get_parser = subparsers.add_parser("get", help="retrieve a snippet")
	get_parser.add_argument("name", help="The name of the snippet")
	get_parser.add_argument("snippet", help="The snippet text")
	get_parser.add_argument("filename", default="snippets.csv", nargs="?",
							help="The source where the snippet exists")
	return parser

def main():
	""" Main function """
	logging.info("Starting Snippets")
	parser = make_parser()
	arguments = parser.parse_args(sys.argv[1:])
	# Convert parsed arguments from Namespace to dictionary
	arguments = vars(arguments)
	command = arguments.pop("command")

	if command == "put":
		name, snippet = put(**arguments)
		print "Stored {!r} as {!r}".format(snippet, name)

	if command == "get":
		name, filename = get(**arguments)
		print "Retrieved {!r} from {!r}".format(name, filename)

if __name__ == '__main__':
	main()