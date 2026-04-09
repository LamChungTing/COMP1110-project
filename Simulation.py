class Customer:
    def __init__(self, party_size, arrival_time, dining_time, max_waiting_time):
        self.party_size = int(party_size)
        self.arrival_time = self._convert_to_minutes(arrival_time)
        self.dining_time = int(dining_time)
        self.max_waiting_time = int(max_waiting_time)

    def _convert_to_minutes(self, time_str):
        hours, minutes = map(int, time_str.strip().split(':'))
        return hours * 60 + minutes

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


customers = open_customer_data("customers.txt")
