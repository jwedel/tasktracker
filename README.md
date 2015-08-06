# tasktracker

Command-line based tool to track work tasks. This is a helper tool for people who need to track work tasks for an employer or customer in a special inconvienient tool. `tasktracker` is easy to use and fast and you can use it to track your task easily across a week and then enter all work into that inconvenient tool.

# Start on windows:

Double click on starter.bat

This opens a shell:

    ttrack> -h
    usage: ttrack.py [-h] {start,done,list} ...

    Task tracker.
    
    positional arguments:
      {start,done,list}  sub-commands help
        start            Starts the current day
        done             Ends the current running task
        list             List all tasks
    
    optional arguments:
      -h, --help         show this help message and exit
    
    ttrack> start
    Good morning!
    
    ttrack> done "Sprint planning"
    Good job: Sprint planning
    
    ttrack> list
    * 2015-07-30 09:00:42
                 09:30:42 - 00:30 - Sprint planning
