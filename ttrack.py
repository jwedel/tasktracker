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
	list = 3

class Entry:
	def __init__(self, type, date_time, duration, description):
		self.type = type
		self.date_time = date_time
		self.duration = duration
		self.description = description

JOURNAL_FILE_NAME = "journal.txt"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

type_map = {
	"S" : "Start",
	"D" : ""
}

def start_day(journal, args):
	print("Good morning!")
	add_journal_entry("S")

def task_done(journal, args):
	print("Good job: " + args.task_description)

	if len(journal) == 0 :
		print("ERROR: You did not start a new day, unable to calculate the task duration.")
	else:
		current_datetime = datetime.now()
		last_datetime = journal[-1].date_time
		diff = current_datetime - last_datetime
		hours = int(diff / timedelta(hours=1))
		minutes = int(diff / timedelta(minutes=1)) - (hours * 60)

		duration_str =  "%02d:%02d" % (hours,minutes)

		add_journal_entry("D", duration_str, args.task_description)

def add_journal_entry(prefix, duration="", description=""):
	with open(JOURNAL_FILE_NAME, "a") as journal:
		line = ",".join([prefix, datetime.now().isoformat(), duration, description])
		print(line, file=journal)

def list_tasks(journal, args):
	for entry in journal:
		print(entry_to_str(entry))

def entry_to_str(entry):
	type_str = "%6s" % (type_map[entry.type])

	if entry.type == "S":
		datetime_str = entry.date_time.strftime("%Y-%m-%d %H:%M:%S")
		entry_str = "* %10s" % (datetime_str)
	else:
		datetime_str = entry.date_time.strftime("%H:%M:%S")
		entry_str = "    " + " - ".join([datetime_str, entry.duration, entry.description ])

	return entry_str

def handle_command_line():
	parser = argparse.ArgumentParser(description='Task tracker.')

	subparsers = parser.add_subparsers(help='sub-commands help')
	subparsers.dest = "command"
	subparsers.required = True

	parser_start = subparsers.add_parser(Commands.start.name, help='Starts the current day')

	parser_done = subparsers.add_parser(Commands.done.name, help='Ends the current running task')
	parser_done.add_argument('task_description', type=str, help='A short description of the task that is done.')

	parser_list = subparsers.add_parser(Commands.list.name, help='List all tasks')

	return parser.parse_args()

def parse_journal(journal_lines):
	
	def split_line(line):
		(entry_type, entry_date_time_str, entry_duration, entry_description) = line.strip().split(",", 3)

		entry_date_time = datetime.strptime(entry_date_time_str, DATE_FORMAT )

		return Entry(entry_type, entry_date_time, entry_duration, entry_description)

	return [split_line(first) for first in journal_lines]

def read_journal(file_name):
	with open(file_name) as f:
		journal_lines = f.readlines()

	return journal_lines

if __name__ == "__main__":
	args = handle_command_line()

	commands_functions = {
		Commands.start.name : start_day,
		Commands.done.name : task_done,
		Commands.list.name : list_tasks
	}

	if os.path.isfile(JOURNAL_FILE_NAME):
		journal_lines = read_journal(JOURNAL_FILE_NAME)

		journal = parse_journal(journal_lines)
	else:
		journal = []

	commands_functions[args.command](journal, args)
