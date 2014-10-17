import logging, csv
# import csv
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="output.log", level=logging.DEBUG)

# Create a function to write the snippet
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

# Create the fucntion to read a snippet
def get(name, filename):
	logging.info("Retreiving {!r} to {!r}".format(name, filename))
	logging.debug("Opening and reading file")
	with open(filename, "r") as f:
		reader = csv.reader(f, delimiter=",")
		logging.debug("Reading file for snippet")
		for row in reader:
			if row[0] == name:
				return name, row[1]
	return name, "Error!"

# Create the parsers for command line execution
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

	# Create the 'get' subparser
	logging.debug("Constructing get parser")
	get_parser = subparsers.add_parser("get", help="retrieve a snippet")
	get_parser.add_argument("name", help="The name of the snippet")
	# get_parser.add_argument("snippet", help="The snippet text")
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
		name, snippet = get(**arguments)
		if snippet == "Error!":
			print "Could not find snippet '{}'".format(arguments["name"])
		else:
			print "Retrieved '{}' as '{}'".format(snippet, name)
		# else: 
		# 	print "Retrieved {!r} from {!r}".format(snippet, name)

if __name__ == '__main__':
	main()