class Customer:
    def __init__(self, party_size, arrival_time, dining_time, max_waiting_time):
        self.party_size = int(party_size)
        self.arrival_time = self._convert_to_minutes(arrival_time)
        self.dining_time = int(dining_time)
        self.max_waiting_time = int(max_waiting_time)

    def _convert_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.strip().split(':'))
        return hours * 60 + minutes
    def __repr__(self):
        return f"Customer(party_size={self.party_size}, arrival_time={self.arrival_time}, dining_time={self.dining_time}, max_waiting_time={self.max_waiting_time})\n"

#reading the data
def open_customer_data(file_path):
    customer_array = []
    
    try:
        with open(file_path, 'r') as file:
            # Skip header line
            next(file) 
            for line in file:
                data = line.strip().split(',')
                # validation
                if len(data) == 4:
                    new_customer = Customer(
                        party_size=data[0],
                        arrival_time=data[1],
                        dining_time=data[2],
                        max_waiting_time=data[3]
                    )
                    customer_array.append(new_customer)
                    
            return customer_array

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    

def open_resturant_data(file_path): 
    table_counts = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    count = int(line.split(':')[1].strip())
                    table_counts.append(count)
        return table_counts
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []



customers = open_customer_data("queue.txt")
tables = open_resturant_data("tables.txt")

print(tables)

#algorithm
avg_wait_time = 0
max_queue_length = 0
tbl_utilization = 0
longest_wait_time = 0
logs = ""





#output data (output file is "output.txt")
with open("output.txt", 'a') as file:
    file.write(f"Avg wait time: {avg_wait_time}\n")
    file.write(f"Max queue length: {max_queue_length}\n") 
    file.write(f"Table utilization: {tbl_utilization}\n") 
    file.write(f"Longest wait time: {longest_wait_time}\n") 
    file.write(f"Logs: {logs}\n")