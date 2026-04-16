"""
Restaurant Queue Simulation System
Simulates customer seating, waiting times, and table utilization.
"""

class Customer:
    """Represents a customer party with their arrival and dining preferences."""
    
    def __init__(self, party_size, arrival_time_str, dining_time_minutes, max_waiting_time_minutes):
        self.party_size = int(party_size)
        self.arrival_time = self._convert_to_minutes(arrival_time_str)
        self.dining_time = int(dining_time_minutes)
        self.max_waiting_time = int(max_waiting_time_minutes)
    
    def _convert_to_minutes(self, time_string):
        """Converts HH:MM to minutes from midnight."""
        hours, minutes = map(int, time_string.strip().split(':'))
        return hours * 60 + minutes

def format_time(minutes):
    """Converts minutes from midnight back to HH:MM."""
    h = int(minutes // 60) % 24
    m = int(minutes % 60)
    return f"{h:02d}:{m:02d}"

def format_duration(minutes):
    """Converts a duration in minutes to HH:MM format."""
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h:02d}:{m:02d}"

def OpenCustomerData(file_path):
    customer_array = []
    try:
        with open(file_path, 'r') as file:
            next(file) 
            for line in file:
                data = line.strip().split(',')
                if len(data) == 4:
                    new_customer = Customer(data[0], data[1], data[2], data[3])
                    customer_array.append(new_customer)
        return customer_array
    except FileNotFoundError:
        return []

def OpenRestaurantData(file_path):
    table_counts = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if ':' in line:
                    count = int(line.split(':')[1].strip())
                    table_counts.append(count)
        return table_counts
    except FileNotFoundError:
        return []

def RunSimpleSimulation(customers, table_counts):
    customers = sorted(customers, key=lambda customer: customer.arrival_time)
    
    tables = []
    for _ in range(table_counts[0]):
        tables.append({"type": "small", "capacity": 2, "occupied_until": 0, "total_occupied_time": 0})
    for _ in range(table_counts[1]):
        tables.append({"type": "medium", "capacity": 4, "occupied_until": 0, "total_occupied_time": 0})
    for _ in range(table_counts[2]):
        tables.append({"type": "large", "capacity": 100, "occupied_until": 0, "total_occupied_time": 0})
    
    start_time = customers[0].arrival_time if customers else 0
    current_time = start_time
    
    # ========== Size-based queues (plain Python lists) ==========
    # Small parties: 1-2, Medium: 3-4, Large: 5+
    queue_small = []      # will hold Customer objects
    queue_medium = []
    queue_large = []
    all_queues = [queue_small, queue_medium, queue_large]   # for iteration
    
    total_wait_time = 0
    max_queue_length = 0
    longest_wait_time = 0
    longest_was_abandoned = False
    simulation_logs = []
    served_customers = 0
    abandoned_customers = 0
    customer_index = 0
    
    # Helper to update max queue length (sum of all queues)
    def update_max_queue_length():
        total_len = len(queue_small) + len(queue_medium) + len(queue_large)
        nonlocal max_queue_length
        if total_len > max_queue_length:
            max_queue_length = total_len
    
    # Helper to add a customer to the correct queue
    def enqueue_customer(cust):
        if cust.party_size <= 2:
            queue_small.append(cust)
        elif cust.party_size <= 4:
            queue_medium.append(cust)
        else:
            queue_large.append(cust)
        update_max_queue_length()
    
    # LOOP: continue while there are customers OR any queue is non‑empty OR tables are occupied
    while (customer_index < len(customers) or 
           any(q for q in all_queues) or 
           any(t['occupied_until'] > 0 for t in tables)):
        
        # 1. Free tables and log completion
        for table in tables:
            if 0 < table['occupied_until'] <= current_time:
                finish_time = table['occupied_until']
                table['occupied_until'] = 0
                simulation_logs.append(f"Time {format_time(finish_time)}: Table ({table['type']}) became available")
        
        # 2. Arrivals
        while (customer_index < len(customers) and customers[customer_index].arrival_time == current_time):
            cust = customers[customer_index]
            enqueue_customer(cust)
            simulation_logs.append(f"Time {format_time(current_time)}: Party of {cust.party_size} arrived. Queue sizes: S:{len(queue_small)} M:{len(queue_medium)} L:{len(queue_large)}")
            customer_index += 1
        
        # 3. Abandonment (check all three queues)
        for q in all_queues:
            still_waiting = []
            for cust in q:
                deadline = cust.arrival_time + cust.max_waiting_time
                if current_time >= deadline:
                    abandoned_customers += 1
                    total_wait_time += cust.max_waiting_time
                    if cust.max_waiting_time > longest_wait_time:
                        longest_wait_time = cust.max_waiting_time
                        longest_was_abandoned = True
                    simulation_logs.append(f"Time {format_time(deadline)}: Party of {cust.party_size} ABANDONED! (Waited {cust.max_waiting_time} min)")
                else:
                    still_waiting.append(cust)
            q[:] = still_waiting   # replace queue content
        update_max_queue_length()
        
        # 4. Seating – try to seat customers, giving priority to small then medium then large
        seated_someone = False
        # Keep trying until no queue can seat its head
        while True:
            seated_this_round = False
            # Check queues in priority order: small → medium → large
            for q in all_queues:
                if not q:
                    continue
                cust = q[0]   # peek at the first waiting customer in this queue
                # Find a free table that can accommodate this party
                suitable_tables = [t for t in tables if t['occupied_until'] == 0 and t['capacity'] >= cust.party_size]
                if suitable_tables:
                    # Remove from queue (FCFS within the queue) using pop(0) – simple list operation
                    q.pop(0)
                    chosen_table = min(suitable_tables, key=lambda t: t['capacity'])
                    wait_time = current_time - cust.arrival_time
                    chosen_table['occupied_until'] = current_time + cust.dining_time
                    chosen_table['total_occupied_time'] += cust.dining_time
                    total_wait_time += wait_time
                    if wait_time > longest_wait_time:
                        longest_wait_time = wait_time
                        longest_was_abandoned = False
                    served_customers += 1
                    seated_someone = True
                    seated_this_round = True
                    simulation_logs.append(f"Time {format_time(current_time)}: Party of {cust.party_size} seated at {chosen_table['type']}. Wait: {wait_time} min")
                    break   # seated one, restart from small queue priority
            if not seated_this_round:
                break   # no one could be seated now
        
        # 5. Jump to next event (arrival, table free, or abandonment)
        next_times = []
        if customer_index < len(customers):
            next_times.append(customers[customer_index].arrival_time)
        for table in tables:
            if table['occupied_until'] > current_time:
                next_times.append(table['occupied_until'])
        # Add abandonment deadlines for all waiting customers
        for q in all_queues:
            for cust in q:
                next_times.append(cust.arrival_time + cust.max_waiting_time)
        
        if next_times:
            next_event = min(next_times)
            # Advance time: at least 1 minute if we seated someone, otherwise jump directly to next_event
            if seated_someone:
                current_time = max(current_time + 1, next_event)
            else:
                current_time = max(current_time, next_event)
        else:
            break

    # Final Statistics
    duration = current_time - start_time
    total_customers = served_customers + abandoned_customers
    avg_wait = total_wait_time / total_customers if total_customers > 0 else 0
    utilization = (sum(t['total_occupied_time'] for t in tables) / (len(tables) * duration) * 100) if duration > 0 else 0
    
    longest_wait_msg = f"{longest_wait_time}" + (" (Abandoned)" if longest_was_abandoned else "")
    
    simulation_logs.append(f"\n=== STATISTICS ===")
    simulation_logs.append(f"Served customers: {served_customers}")
    simulation_logs.append(f"Abandoned customers: {abandoned_customers}")
    simulation_logs.append(f"Total customers processed: {total_customers}")
    simulation_logs.append(f"Total simulation time: {duration} minutes ({format_duration(duration)})")
    
    return (avg_wait, max_queue_length, utilization, longest_wait_msg, "\n".join(simulation_logs))

# ============ MAIN EXECUTION ============
customers = OpenCustomerData("queue.txt")
restaurant_tables = OpenRestaurantData("tables.txt")

(avg_wait, max_q, util, longest_info, logs) = RunSimpleSimulation(customers, restaurant_tables)

with open("output.txt", 'w') as f:
    f.write(f"Average wait time: {avg_wait:.2f} minutes\n")
    f.write(f"Maximum queue length: {max_q} parties\n")
    f.write(f"Table utilization: {util:.2f}%\n")
    f.write(f"Longest wait time: {longest_info} minutes\n")
    f.write(f"\n=== SIMULATION LOGS ===\n")
    f.write(logs)

print("Simulation complete! Output written to output.txt")