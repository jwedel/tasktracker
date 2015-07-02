# S 2015-07-01T09:00:00 
# D 2015-07-01T09:10:00 Worked on Bursa
# D 2015-07-01T09:10:00 Blue ant
# E 2015-07-01T09:00:00


import argparse
import re
import os.path

from datetime import datetime, timedelta
from enum import Enum
from time import time

class Commands(Enum):
	start = 1
	done = 2

JOURNAL_FILE_NAME = "journal.txt"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

def start_day(journal, args):
	print("Good morning!")
	add_journal_entry("S")

def task_done(journal, args):
	print("Good job: " + args.task_description)

	if len(journal) == 0 :
		print("ERROR: You did not start a new day, unable to calculate the task duration.")
	else:
		current_datetime = datetime.now()
		last_datetime = journal[-1][1]
		diff = current_datetime - last_datetime
		hours = int(diff / timedelta(hours=1))
		minutes = int(diff / timedelta(minutes=1)) - (hours * 60)

		duration_str =  "%02d:%02d" % (hours,minutes)

		add_journal_entry("D", duration_str + " " + args.task_description)

def add_journal_entry(prefix, description=""):
	with open(JOURNAL_FILE_NAME, "a") as journal:
		line = " ".join([prefix, datetime.now().isoformat(), description])
		print(line, file=journal)

def handle_command_line():
	parser = argparse.ArgumentParser(description='Task tracker.')

	subparsers = parser.add_subparsers(help='sub-commands help')
	subparsers.dest = "command"

	parser_start = subparsers.add_parser(Commands.start.name, help='Starts the current day')

	parser_done = subparsers.add_parser(Commands.done.name, help='Ends the current running task')
	parser_done.add_argument('task_description', type=str, help='A short description of the task that is done.')

	return parser.parse_args()

def parse_journal(journal_lines):
	
	def split_line(line):
		entry_fields = line.split(" ", 2)

		if len(entry_fields) < 2:
			raise Exception("Illegal journal entry found: " + line)

		entry_type = entry_fields[0]

		entry_date_time = datetime.strptime(entry_fields[1], DATE_FORMAT )

		if len(entry_fields) > 2:
			entry_description = entry_fields[2]
		else:
			entry_description = None

		print(entry_type, entry_date_time, entry_description)

		return (entry_type, entry_date_time, entry_description)

	return [split_line(first) for first in journal_lines]

def read_journal(file_name):
	with open(file_name) as f:
		journal_lines = f.readlines()

	return journal_lines

if __name__ == "__main__":
	args = handle_command_line()

	print(args)

	commands_functions = {
		Commands.start.name : start_day,
		Commands.done.name : task_done
	}

	if os.path.isfile(JOURNAL_FILE_NAME):
		journal_lines = read_journal(JOURNAL_FILE_NAME)

		journal = parse_journal(journal_lines)
	else:
		journal = []

	commands_functions[args.command](journal, args)
