# tasktracker

Command-line based tool to track work tasks. This is a helper tool for people who need to track work tasks for an employer or customer in a special inconvienient tool. `tasktracker` is easy to use and fast and you can use it to track your task easily across a week and then enter all work into that inconvenient tool.

# Prerequisites

Python 3 must be installed and available on your system path. To check, open a Windows shell `cmd.exe`:


    C:\>python
    Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 24 2015, 22:43:06) [MSC v.1600 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()
    
    C:\>

# Start on windows:

Double click on starter.bat (Thanks to cab)

This opens a shell. 

## Get some help:

    ttrack> -h

    usage: ttrack.py [-h] {start,st,done,dn,list,ls} ...

    Task tracker.

    positional arguments:
      {start,st,done,dn,list,ls}
                            sub-commands help
        start (st)          Starts the current day
        done (dn)           Ends the current running task
        list (ls)           List all tasks

    optional arguments:
      -h, --help            show this help message and exit

## get gelp on a specific command (e.g. start):

    ttrack> start -h
    usage: ttrack.py start [-h] [HH[:MM[:SS]]]
    
    positional arguments:
      HH[:MM[:SS]]  Allows to provide the start time for today.
    
## Start the day (required)

    ttrack> start
    Good morning!
    
As an alternative, you can specify the time:

    ttrack> start 9
    Good morning!

Finish a job now (will calculate the time difference last job till now):

    ttrack> done "Sprint planning"
    Good job: Sprint planning
    
Or you can finish a you specifying the duration:
    
    ttrack> done -d 1hr30m "Sprint planning"
    Good job: Sprint planning

Finish another job, quotes are only required for descriptions with spaces:
    
    ttrack> done Lunch
    Good job: Lunch

List your journal:    

    ttrack> list
    * 2015-07-30 09:00:42
                 10:30:42 - 01:30 - Sprint planning
                 11:00:42 - 00:30 - Lunch

## Aliases

There are short aliases for all command:

|Command|Alias|
|---|---|
|start|st|
|done|dn|
|list|ls| 

