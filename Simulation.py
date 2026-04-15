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
                        party_size = data[0],
                        arrival_time = data[1],
                        dining_time = data[2],
                        max_waiting_time = data[3]
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

def open_resturant_data(file_path):
    dict(resturnat_tables)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                resturant_tables[data[0]] = data[1] 
    
customers = open_customer_data("queue.txt")
tables = open_resturant_data("tables.txt")


#output metrics
avg_wait_time = 0
max_queue_length = 0
tbl_utilization = 0
longest_wait_time = 0
logs = ""

#simple queuing algorithm
def run_simple_simulation(customers, table_counts):

    customers = sorted(customers, key = lambda c: c.arrival_time)
    
    # Create individual tables
    tables = []
    # (1-2 persons)
    for i in range(table_counts[0]):
        tables.append({"type": "small", "capacity": 2, "occupied_until": 0, "total_occupied_time": 0})
    # (3-4 persons)
    for i in range(table_counts[1]):
        tables.append({"type": "medium", "capacity": 4, "occupied_until": 0, "total_occupied_time": 0})
    # (5+ persons)
    for i in range(table_counts[2]):
        tables.append({"type": "large", "capacity": 100, "occupied_until": 0, "total_occupied_time": 0})
    
    queue = []
    current_time = 0
    total_wait_time = 0
    max_queue_length = 0
    longest_wait_time = 0
    logs = []
    served_customers = 0
    abandoned_customers = 0
    i = 0
    
    while i < len(customers) or queue or any(t['occupied_until'] > current_time for t in tables):
        
        # Free up tables
        for table in tables:
            if table['occupied_until'] <= current_time and table['occupied_until'] > 0:
                table['occupied_until'] = 0
                logs.append(f"Time {current_time}: Table ({table['type']}) became available")
        
        # Add arriving customers
        while i < len(customers) and customers[i].arrival_time <= current_time:
            queue.append(customers[i])
            logs.append(f"Time {current_time}: Party of {customers[i].party_size} arrived. Queue: {len(queue)}")
            i += 1
        
        max_queue_length = max(max_queue_length, len(queue))
        
        # Try to seat customers
        seated = False
        queue_copy = queue.copy()
        
        for customer in queue_copy:
            # Find suitable table
            suitable_tables = [t for t in tables if t['occupied_until'] == 0 and t['capacity'] >= customer.party_size]
            
            if suitable_tables:
                # Choose smallest suitable table
                table = min(suitable_tables, key=lambda t: t['capacity'])
                queue.remove(customer)
                seated = True
                
                wait_time = current_time - customer.arrival_time
                
                # Check abandonment
                if wait_time > customer.max_waiting_time:
                    abandoned_customers += 1
                    logs.append(f"Time {current_time}: Party of {customer.party_size} ABANDONED (waited {wait_time} min)")
                    continue
                
                # Seat customer
                table['occupied_until'] = current_time + customer.dining_time
                table['total_occupied_time'] += customer.dining_time
                total_wait_time += wait_time
                longest_wait_time = max(longest_wait_time, wait_time)
                served_customers += 1
                
                logs.append(f"Time {current_time}: Party of {customer.party_size} seated at {table['type']} table. Wait: {wait_time} min. Dining: {customer.dining_time} min")
        
        # Advance time
        if not seated and (queue or i < len(customers)):
            next_times = []
            if i < len(customers):
                next_times.append(customers[i].arrival_time)
            for table in tables:
                if table['occupied_until'] > current_time:
                    next_times.append(table['occupied_until'])
            current_time = min(next_times)
        elif not seated and not queue and i >= len(customers):
            break
        elif seated:
            # Continue with same time to seat more
            pass
    
    # Calculate utilization
    total_simulation_time = current_time
    total_possible_time = len(tables) * total_simulation_time
    total_actual_time = sum(t['total_occupied_time'] for t in tables)
    tbl_utilization = (total_actual_time / total_possible_time * 100) if total_possible_time > 0 else 0
    
    avg_wait_time = total_wait_time / served_customers if served_customers > 0 else 0

    return avg_wait_time, max_queue_length, tbl_utilization, longest_wait_time, "\n".join(logs)

#run simple queue simulation
avg_wait_time, max_queue_length, tbl_utilization, longest_wait_time, logs = run_simple_simulation(customers, tables)

#output data (output file is "output.txt")
with open("output.txt", 'w') as file:  
    file.write(f"Avg wait time: {avg_wait_time:.2f}\n") 
    file.write(f"Max queue length: {max_queue_length}\n") 
    file.write(f"Table utilization: {tbl_utilization:.2f}%\n") 
    file.write(f"Longest wait time: {longest_wait_time}\n") 
    file.write(f"\n=== SIMULATION LOGS ===\n")
    file.write(logs)  

