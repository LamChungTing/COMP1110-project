"""
Restaurant Queue Simulation System
Simulates customer seating, waiting times, and table utilization for a restaurant.
"""

class Customer:
    """Represents a customer party with their arrival and dining preferences."""
    
    def __init__(self, party_size, arrival_time_str, dining_time_minutes, max_waiting_time_minutes):
        """
        Initialize a Customer object.
        
        Args:
            party_size (str): Number of people in the party
            arrival_time_str (str): Time in format "HH:MM"
            dining_time_minutes (str): How long they will eat (minutes)
            max_waiting_time_minutes (str): Maximum minutes they'll wait before leaving
        """
        self.party_size = int(party_size)
        self.arrival_time = self._convert_to_minutes(arrival_time_str)
        self.dining_time = int(dining_time_minutes)
        self.max_waiting_time = int(max_waiting_time_minutes)
    
    def _convert_to_minutes(self, time_string):
        """
        Convert time string "HH:MM" to minutes since midnight.
        
        Example: "14:30" -> 870 minutes (14*60 + 30)
        
        Args:
            time_string (str): Time in format "HH:MM"
            
        Returns:
            int: Minutes since midnight
        """
        hours, minutes = map(int, time_string.strip().split(':'))
        return hours * 60 + minutes
    
    def __repr__(self):
        """String representation for debugging."""
        return f"Customer(party_size={self.party_size}, arrival_time={self.arrival_time}, dining_time={self.dining_time}, max_waiting_time={self.max_waiting_time})\n"


def OpenCustomerData(file_path):
    """
    Read customer data from a CSV file.
    
    Expected file format:
    - Header row (skipped)
    - Each row: party_size,arrival_time,dining_time,max_waiting_time
    
    Args:
        file_path (str): Path to the customer data file
        
    Returns:
        list: Array of Customer objects, empty list if file not found
    """
    customer_array = []
    
    try:
        with open(file_path, 'r') as file:
            # Skip the header line (column names)
            next(file) 
            
            for line in file:
                # Split CSV line into individual values
                data = line.strip().split(',')
                
                # Only process lines with exactly 4 values
                if len(data) == 4:
                    new_customer = Customer(
                        party_size=data[0],
                        arrival_time_str=data[1],
                        dining_time_minutes=data[2],
                        max_waiting_time_minutes=data[3]
                    )
                    customer_array.append(new_customer)
                    
        return customer_array

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []


def OpenRestaurantData(file_path):
    """
    Read table configuration from a text file.
    
    Expected file format:
    Small:2
    Medium:4
    Large:100
    
    Args:
        file_path (str): Path to the restaurant data file
        
    Returns:
        list: Array of table counts [small_tables, medium_tables, large_tables]
    """
    table_counts = []
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Look for lines containing a colon (key:value format)
                if ':' in line:
                    # Extract the number after the colon
                    count = int(line.split(':')[1].strip())
                    table_counts.append(count)
                    
        return table_counts
        
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []


def RunSimpleSimulation(customers, table_counts):
    """
    Run the main restaurant seating simulation using First Come First Serve.
    
    The algorithm:
    1. Processes customers in arrival order
    2. Maintains a queue of waiting customers
    3. ONLY the FIRST person in line can be seated
    4. Tracks wait times, queue lengths, and table utilization
    5. Handles customer abandonment if wait time exceeds their limit
    
    Args:
        customers (list): Array of Customer objects
        table_counts (list): [small_tables, medium_tables, large_tables]
        
    Returns:
        tuple: (average_wait_time, max_queue_length, table_utilization_percent, 
                longest_wait_time, simulation_logs)
    """
    
    # Sort customers by arrival time (earliest first)
    customers = sorted(customers, key=lambda customer: customer.arrival_time)
    
    # Create individual table objects from the counts
    tables = []
    
    # Create small tables (for 1-2 persons)
    for _ in range(table_counts[0]):
        tables.append({
            "type": "small", 
            "capacity": 2, 
            "occupied_until": 0,          # Time when table becomes free (0 = free now)
            "total_occupied_time": 0       # Total minutes table was used
        })
    
    # Create medium tables (for 3-4 persons)
    for _ in range(table_counts[1]):
        tables.append({
            "type": "medium", 
            "capacity": 4, 
            "occupied_until": 0, 
            "total_occupied_time": 0
        })
    
    # Create large tables (for 5+ persons)
    for _ in range(table_counts[2]):
        tables.append({
            "type": "large", 
            "capacity": 100, 
            "occupied_until": 0, 
            "total_occupied_time": 0
        })
    
    # Simulation state variables
    waiting_queue = []             # Customers waiting to be seated
    current_time = 0               # Current simulation time in minutes
    total_wait_time = 0            # Sum of all wait times (for average calculation)
    max_queue_length = 0           # Longest the queue ever got
    longest_wait_time = 0          # Maximum wait time any customer experienced
    simulation_logs = []           # List of all events that happened
    served_customers = 0           # Count of customers who were seated
    abandoned_customers = 0        # Count of customers who left due to long wait
    customer_index = 0             # Next customer to consider for arrival
    
    # Main simulation loop - continues while:
    # - There are customers waiting to arrive OR
    # - There are customers in the queue OR
    # - Any tables are currently occupied
    while (customer_index < len(customers) or 
           waiting_queue or 
           any(table['occupied_until'] > current_time for table in tables)):
        
        # STEP 1: Free up any tables that have finished dining
        for table in tables:
            # If table's occupied time is up AND it was actually occupied
            if table['occupied_until'] <= current_time and table['occupied_until'] > 0:
                table['occupied_until'] = 0  # Mark as free
                simulation_logs.append(f"Time {current_time}: Table ({table['type']}) became available")
        
        # STEP 2: Process new customer arrivals at this time
        while (customer_index < len(customers) and 
               customers[customer_index].arrival_time <= current_time):
            # Customer arrives - add them to the waiting queue
            waiting_queue.append(customers[customer_index])
            simulation_logs.append(
                f"Time {current_time}: Party of {customers[customer_index].party_size} arrived. "
                f"Queue: {len(waiting_queue)}"
            )
            customer_index += 1
        
        # Track the maximum queue length seen so far
        max_queue_length = max(max_queue_length, len(waiting_queue))
        
        # ========== STEP 3: FIRST COME FIRST SERVE SEATING ==========
        seated_someone = False
        
        # ONLY look at the FIRST person in line (if queue is not empty)
        if waiting_queue:
            customer = waiting_queue[0]  # Look at front of queue only
            
            # Find all tables that are:
            # 1. Currently free (occupied_until == 0)
            # 2. Large enough for the party
            suitable_tables = [
                table for table in tables 
                if table['occupied_until'] == 0 and table['capacity'] >= customer.party_size
            ]
            
            if suitable_tables:
                # Choose the smallest table that fits (best fit algorithm)
                chosen_table = min(suitable_tables, key=lambda table: table['capacity'])
                
                # Remove the FIRST customer from the queue (pop from front)
                waiting_queue.pop(0)
                seated_someone = True
                
                # Calculate how long this customer waited
                wait_time = current_time - customer.arrival_time
                
                # Check if customer gave up waiting
                if wait_time > customer.max_waiting_time:
                    abandoned_customers += 1
                    simulation_logs.append(
                        f"Time {current_time}: Party of {customer.party_size} ABANDONED "
                        f"(waited {wait_time} min, max was {customer.max_waiting_time} min)"
                    )
                    # Don't seat them, but continue the loop (don't set seated_someone to False)
                    # We already set seated_someone = True above, but we need to undo it
                    seated_someone = False
                    continue  # Skip seating this customer
                
                # Seat the customer at the chosen table
                chosen_table['occupied_until'] = current_time + customer.dining_time
                chosen_table['total_occupied_time'] += customer.dining_time
                total_wait_time += wait_time
                longest_wait_time = max(longest_wait_time, wait_time)
                served_customers += 1
                
                simulation_logs.append(
                    f"Time {current_time}: Party of {customer.party_size} seated at "
                    f"{chosen_table['type']} table. Wait: {wait_time} min. "
                    f"Dining: {customer.dining_time} min"
                )
        # ========== END OF FCFS SEATING LOGIC ==========
        
        # STEP 4: Advance time to the next interesting event
        if not seated_someone and (waiting_queue or customer_index < len(customers)):
            # No one was seated, but there are pending events
            next_event_times = []
            
            # Add the next customer's arrival time
            if customer_index < len(customers):
                next_event_times.append(customers[customer_index].arrival_time)
            
            # Add when each occupied table will become free
            for table in tables:
                if table['occupied_until'] > current_time:
                    next_event_times.append(table['occupied_until'])
            
            # Jump to the soonest future event
            current_time = min(next_event_times)
            
        elif not seated_someone and not waiting_queue and customer_index >= len(customers):
            # No customers left and nothing is happening - simulation is done
            break
            
        elif seated_someone:
            # We seated someone - continue at the same time to try seating more
            # (other tables might still be free for other customers)
            pass
    
    # STEP 5: Calculate final statistics
    
    # Table Utilization = (actual occupied time) / (maximum possible time) * 100
    total_simulation_time = current_time
    total_possible_time = len(tables) * total_simulation_time
    total_actual_time = sum(table['total_occupied_time'] for table in tables)
    
    # Avoid division by zero
    if total_possible_time > 0:
        table_utilization_percent = (total_actual_time / total_possible_time * 100)
    else:
        table_utilization_percent = 0
    
    # Average wait time (avoid division by zero)
    if served_customers > 0:
        average_wait_time = total_wait_time / served_customers
    else:
        average_wait_time = 0
    
    # Print abandonment statistics (optional)
    if abandoned_customers > 0:
        print(f"Note: {abandoned_customers} customer(s) abandoned due to long wait times")
    
    return (average_wait_time, max_queue_length, table_utilization_percent, 
            longest_wait_time, "\n".join(simulation_logs))


# ============ MAIN EXECUTION ============

# Load data from files
customers = OpenCustomerData("queue.txt")
restaurant_tables = OpenRestaurantData("tables.txt")

# Run the simulation
(average_wait_time, max_queue_length, table_utilization, 
 longest_wait_time, simulation_logs) = RunSimpleSimulation(customers, restaurant_tables)

# Write results to output file
with open("output.txt", 'w') as output_file:
    output_file.write(f"Average wait time: {average_wait_time:.2f} minutes\n")
    output_file.write(f"Maximum queue length: {max_queue_length} parties\n")
    output_file.write(f"Table utilization: {table_utilization:.2f}%\n")
    output_file.write(f"Longest wait time: {longest_wait_time} minutes\n")
    output_file.write(f"\n=== SIMULATION LOGS ===\n")
    output_file.write(simulation_logs)

print("Simulation complete! Check output.txt for results.")