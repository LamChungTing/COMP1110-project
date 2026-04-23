Restaurant queueing simulation

This project aims to create a simulation on different queueing methods in different restaurants to analyse the most efficient queueing methods based on different restaurant settings and customer flow.

language used: Python

the execution environment: terminal / any Python IDE

Compilation/setup instructions: When using the program, make sure to fill in Tables.txt, and either queue.txt or queueVIP.txt according to the format included in line 1, depending on the simulation program you want to do. Do not delete line 1. Make sure you do not mix up the txt files – queue.txt is for FirstComeFirstServe.py and SizedBasedQueue.py, queueVIP.txt is for VIPqueue.py. Output will be in Output.txt.

Purposes for the different files
FirstComeFirstServe.py
Inputs data from Queue.txt and Tables.txt, and run the simulation of a first come first serve customer seating queue, and append the data and statistics in Output.txt
SizedBasedQueue.py
Inputs data from Queue.txt and Tables.txt, and simulate a size-based customer seating queue, and append the data and statistics in Output.txt
VIPqueue.py
Inputs data from Queue.txt and Tables.txt, and run a queueing system where VIP gets higher priority and can be served first, and append the data and statistics in Output.txt
Queue.txt
Input file containing 4 columns, party size, arrival time, dining time and max waiting time, used in FirstComeFirstServe.py and SizedBasedQueue.py 
queueVIP.txt
Input file similar to queue.txt, but added a VIP to identify what party has priority, used in VIPqueue.py
Tables.txt
Basic input file with how many 1-2, 3-4, and 5+ tables are there in the restaurant
Output.txt
The final output file generated after running the programs, it will include average wait time, max queue length, table utilisation (efficiency in using tables), the longest wait time, and a simulation log to show the timeline of queueing, S,M, and L represents the number of small , medium and large parties in the queue

How to run the program: Input queue and table information into queue.txt/VIPqueue.txt and table.txt, simply run the queuing method of choice and output.txt should be generated, the final simulation statistics are in output.txt.

Sample test case: Running FirstComeFirstServe.py
Tables.txt:
1-2 person tables: 2
3-4 person tables: 1
5+ person tables: 1

Queue.txt:
PartySize,ArrivalTime,DiningTime,MaxWaitTime
2,12:00,30,15
2,12:05,30,15
4,12:10,45,10
2,12:12,20,5
10,12:15,60,20
2,12:20,30,10


Ouput.txt:
Average wait time: 4.50 minutes
Maximum queue length: 2 parties
Table utilization: 50.27%
Longest wait time: 17 minutes

=== SIMULATION LOGS ===
Time 12:00: Party of 2 (VIP) arrived. Queue sizes: S:1 M:0 L:0
Time 12:00: Party of 2 seated at small. Wait: 0 min
Time 12:05: Party of 2 arrived. Queue sizes: S:1 M:0 L:0
Time 12:05: Party of 2 seated at small. Wait: 0 min
Time 12:10: Party of 4 arrived. Queue sizes: S:0 M:1 L:0
Time 12:10: Party of 4 seated at medium. Wait: 0 min
Time 12:12: Party of 2 (VIP) arrived. Queue sizes: S:1 M:0 L:0
Time 12:12: Party of 2 seated at large. Wait: 0 min
Time 12:15: Party of 10 (VIP) arrived. Queue sizes: S:0 M:0 L:1
Time 12:20: Party of 2 (VIP) arrived. Queue sizes: S:1 M:0 L:1
Time 12:30: Table (small) became available
Time 12:30: Party of 2 ABANDONED! (Waited 10 min)
Time 12:32: Table (large) became available
Time 12:32: Party of 10 seated at large. Wait: 17 min
Time 12:35: Table (small) became available
Time 12:55: Table (medium) became available
Time 13:32: Table (large) became available

=== STATISTICS ===
Served customers: 5
Abandoned customers: 1
Total customers processed: 6
Total simulation time: 92 minutes (01:32)

