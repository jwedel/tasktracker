# Task tracker

import argparse
import re
import os.path

from datetime import datetime, timedelta, time, date
from enum import Enum

class Commands(Enum):
	start = (1, "st", "Starts the current day")
	done = (2, "dn", "Ends the current running task")
	list = (3, "ls", "List all tasks")

	def get_alias(self):
		return self.value[1]

	def get_help(self):
		return self.value[2]

class Entry:
	def __init__(self, type, date_time, duration, description):
		self.type = type
		self.date_time = date_time
		self.duration = duration
		self.description = description

JOURNAL_FILE_NAME = "journal.txt"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
TIME_REGEX = re.compile(r'(?P<hour>\d+)(:(?P<minute>\d+))?(:(?P<second>\d+))?')
TIME_DIFF_REGEX = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

type_map = {
	"S" : "Start",
	"D" : ""
}

def start_day(journal, args):
	print("Good morning!")
	if not args.start_time:
		start_time = datetime.now()
	else:
		start_time = parse_time(args.start_time)
	add_journal_entry("S", start_time)

def task_done(journal, args):
	print("Good job: " + args.task_description)

	if len(journal) == 0 :
		print("ERROR: You did not start a new day, unable to calculate the task duration.")
	else:
		last_datetime = journal[-1].date_time
		if args.diff:
			diff = parse_time_delta(args.diff)
			current_datetime = last_datetime + diff
		else:
			current_datetime = datetime.now()
			diff = current_datetime - last_datetime
		hours = int(diff / timedelta(hours=1))
		minutes = int(diff / timedelta(minutes=1)) - (hours * 60)

		duration_str =  "%02d:%02d" % (hours,minutes)

		add_journal_entry("D", current_datetime, duration_str, args.task_description)

def add_journal_entry(prefix, current_datetime, duration="", description=""):
	with open(JOURNAL_FILE_NAME, "a") as journal:
		line = ",".join([prefix, current_datetime.isoformat(), duration, description])
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
		entry_str = (" "*13) + " - ".join([datetime_str, entry.duration, entry.description ])

	return entry_str

def parse_time_delta(time_delta_str):
	parts = TIME_DIFF_REGEX.match(time_delta_str)
	if not parts:
		return
	parts = parts.groupdict()
	time_params = {}
	for (name, param) in parts.items():
		if param:
			time_params[name] = int(param)
	return timedelta(**time_params)

def parse_time(time_str):
	parts = TIME_REGEX.match(time_str)
	if not parts:
		return
	parts = parts.groupdict()
	time_params = {}
	for (name, param) in parts.items():
		if param:
			time_params[name] = int(param)
	time_params["microsecond"] = 1
	return datetime.combine(date.today(), time(**time_params))

def handle_command_line():
	parser = argparse.ArgumentParser(description='Task tracker.')

	subparsers = parser.add_subparsers(help='sub-commands help')
	subparsers.dest = "command"
	subparsers.required = True

	parser_start = add_command(subparsers, Commands.start)
	#parser_start = subparsers.add_parser(Commands.start.name, help='Starts the current day', aliases=[Commands.start.get_alias()])
	parser_start.add_argument('start_time', nargs='?', type=str, metavar='HH[:MM[:SS]]', help='Allows to provide the start time for today.')

	parser_done = add_command(subparsers, Commands.done)
	#parser_done = subparsers.add_parser(Commands.done.name, help='Ends the current running task', aliases=[Commands.done.get_alias()])
	parser_done.add_argument('task_description', type=str, help='A short description of the task that is done.')
	parser_done.add_argument('-d', type=str, dest='diff', metavar='HHhr[MMm[SSs]]', help='Allows to provide a timedelta in the form of HHhrMMmSSs. E.g. 1hr or 2hr5m43s')

	parser_list = add_command(subparsers, Commands.list)
	#parser_list = subparsers.add_parser(Commands.list.name, help='List all tasks', aliases=[Commands.list.get_alias()])

	return parser.parse_args()

def add_command(parser, command):
	return parser.add_parser(command.name, help=command.get_help(), aliases=[command.get_alias()])

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
		Commands.list.name : list_tasks,
		Commands.start.get_alias() : start_day,
		Commands.done.get_alias() : task_done,
		Commands.list.get_alias() : list_tasks
	}

	if os.path.isfile(JOURNAL_FILE_NAME):
		journal_lines = read_journal(JOURNAL_FILE_NAME)

		journal = parse_journal(journal_lines)
	else:
		journal = []

	commands_functions[args.command](journal, args)
