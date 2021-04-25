'''
Lai-Yang Algorithm for Global Snapshot Recording
Author: Varisht Ghedia
ID: 2020MT13030

'''
class Process():
    '''
    Process Class
    Initialize using friendly process_number identifier, balance and list of processes as neighbours
    '''

    def __init__(self, p_number, balance, neighbours = []):
        self.p_no = str(p_number)
        self.color = "white"
        self.channel_history = {}
        self.balance = balance
        self.neighbours = neighbours
        self.collected_states = {}
        self.local_state = {}

class Orchestrator():

    '''
    Orchestrator Class
    Used for demonstrating the algorithm. Has methods for sending messages, setting orchestrator and verifying the global snapshot.
    Initialize using the list of all participating processes.
    '''
    
    def __init__(self, process_list):
        self.process_list = process_list
        self.process_list_names = [str(x.p_no) for x in process_list]
        self.orchestrator = None

    def calculate_global_balance(self):
        '''
        Returns the sum of balances of all the processes involved in the algorithm
        '''
        balance = sum([p.balance for p in self.process_list])
        return balance

    def set_orchestrator(self, process):
        '''
        Sets the specified process as the orchestrator of the algorithm.
        Input: process (Process): Process to be set that initiates the algorithm
        '''
        print("P{0} is set as orchestrator for verifying state.".format(process.p_no ))
        self.orchestrator = process
        process.color = 'red'
        # self.process_list_names.remove(process.p_no)
        print("Processes for verification are: ",self.process_list_names)
        # Load the local state into global state list for compare
        process.collected_states[process.p_no] = [process.local_state]
        process.local_state = {}
        

    def verify_states(self, process):
        '''
        Verifies the global state by computing the net sum of the transfers from the local states.
        For consistent state net sum should be 0.

        Input: process (Process): Orchestrator process which collects the local states
        '''
        state_sum = 0
        # Appending self local state for verifying
        collected_states = process.collected_states
        # collected_states[process.p_no] = [process.local_state]
        for k,v in collected_states.items():
            for p_no, transacs in v[0].items():
                for value in transacs:
                    state_sum += value

        if state_sum == 0:
            print("Global State is consistent")
        else:
            print("Global State is inconsistent. Mismatch of {0}".format(state_sum))

        # Cleanup
        process.collected_states = {}
        self.orchestrator = None

        for p in self.process_list:
            p.color = 'white'
        

    
    def send_message(self, sender, receiver, amount):

        '''
        Function to send the messages / transfer balance between the process.
        Automatically sets the colors of the receiver process based on the color of the sender process.
        Calls global state verification method once all local states have been gathered.

        '''

        if receiver.p_no in sender.neighbours:

            print("P{0} sends {1} to P{2}.".format(sender.p_no, amount, receiver.p_no))

            if sender.color == 'red':
                # Append orchestrators own local state into global state collection list
                self.orchestrator.collected_states.setdefault(receiver.p_no, []).append(receiver.local_state)
                receiver.local_state = {} if receiver.color != 'red' else receiver.local_state
                receiver.color = 'red'
                collected_state_names = set(self.orchestrator.collected_states.keys())
                print("Collected Local States are: ", collected_state_names)

                if  collected_state_names == set(self.process_list_names):
                    print("Collected all Local States, Verifying Global State.")
                    self.verify_states(self.orchestrator)
                else:
                    print('Not all local states recorded. Waiting for other local states.')

                          
            sender.balance -= amount
            receiver.channel_history.setdefault(sender.p_no, []).append(amount)
            sender.channel_history.setdefault(receiver.p_no, []).append(-amount)

            receiver.local_state.setdefault(sender.p_no, []).append(amount)
            sender.local_state.setdefault(receiver.p_no, []).append(-amount)
            receiver.balance += amount
        
        else:
            print("{0} is not neighbours with {1}. Cannot send message.".format(sender.p_no, receiver.p_no))


# Execution Section

p1 = Process(1, 6000)
p2 = Process(2, 6500)
p3 = Process(3, 7000)
p4 = Process(4, 6800)

p1.neighbours = [p3.p_no, p4.p_no]
p2.neighbours = [p4.p_no]
p3.neighbours = [p1.p_no]
p4.neighbours = [p1.p_no, p2.p_no]

o = Orchestrator([p1, p2, p3, p4])

print("P1 has: ", p1.balance)
print("P2 has: ", p2.balance)
print("P3 has: ", p3.balance)
print("P4 has: ", p4.balance)

print("Combined Balance at start is: {0}".format(o.calculate_global_balance()))

o.send_message(p1, p3, 500)
o.send_message(p2, p4, 600)
o.send_message(p1, p3, 700)
o.set_orchestrator(p1)
o.send_message(p4, p2, 900)
o.send_message(p1, p3, 700)
print("Process colors are: ")
print(p1.color, p2.color, p3.color, p4.color)
o.send_message(p1, p4, 600)
print("Process colors are: ")
print(p1.color, p2.color, p3.color, p4.color)
o.send_message(p3, p4, 330)
print("Process colors are: ")
print(p1.color, p2.color, p3.color, p4.color)
o.send_message(p4, p2, 110)


print("P1 has: ", p1.balance)
print("P2 has: ", p2.balance)
print("P3 has: ", p3.balance)
print("P4 has: ", p4.balance)

print("Combined Balance at end is: {0}".format(o.calculate_global_balance()))
# print(p1.channel_history)
# print(p2.channel_history[4][0:-1])
# print(p3.channel_history)
# print(p1.collected_states)
print("Process colors are: ")
print(p1.color, p2.color, p3.color, p4.color)
