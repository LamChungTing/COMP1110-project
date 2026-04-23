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
