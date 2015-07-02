# S 2015-07-01T09:00:00 
# D 2015-07-01T09:10:00 Worked on Bursa
# D 2015-07-01T09:10:00 Blue ant
# E 2015-07-01T09:00:00


import argparse
from datetime import datetime
from enum import Enum
from time import time

class Commands(Enum):
	start = 1
	end = 2
	done = 3

JOURNAL_FILE_NAME = "journal.txt"


def start_day(args):
	print("Good morning!")
	add_journal_entry("S")

def add_journal_entry(prefix, description=""):	
	with open(JOURNAL_FILE_NAME, "a") as journal:
		line = " ".join([prefix, datetime.now().isoformat(), description])
		print(line, file=journal)

def end_day(args):
	print("Have good evening!")
	add_journal_entry("E", args.task_description)

def task_done(args):
	print("Good job: " + args.task_description)
	add_journal_entry("D", args.task_description)

def handle_command_line():
	parser = argparse.ArgumentParser(description='Task tracker.')

	subparsers = parser.add_subparsers(help='sub-commands help')
	subparsers.dest = "command"

	parser_start = subparsers.add_parser(Commands.start.name, help='Starts the current day')

	parser_done = subparsers.add_parser(Commands.done.name, help='Ends the current running task')
	parser_done.add_argument('task_description', type=str, help='A short description of the task that is done.')

	# create the parser for the "b" command
	parser_end = subparsers.add_parser(Commands.end.name, help='Ends the current day')
	parser_end.add_argument('task_description', type=str, help='A short description of the task that is done.')

	return parser.parse_args()

if __name__ == "__main__":
	args = handle_command_line()

	print(args)

	commands_functions = {
		Commands.start.name : start_day,
		Commands.end.name : end_day,
		Commands.done.name : task_done
	}

	commands_functions[args.command](args)
