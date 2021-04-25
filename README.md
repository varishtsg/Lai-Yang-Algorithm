# Lai-Yang Algorithm for Global Snapshot Recording

## Introduction:
Code has been tested for python 3.8 on Linux. Code should also work on python 3.7+ Windows 10. No Additional libraries or class files are required. All code is self contained in the single file.

To run the code,

`python process.py`

Included in the script are all the steps in the process. Please check the Execution Section.

## Execution:
Processes involved in the algorithm should be initialized with the Process class. A friendly process number or a name and the initial balance should be provided.

Next the neighbours for the process need to be specified. This is done to simulate the distributed system.

An orchestrator for the algorithm can be initialized using the Orchestrator class. This object takes the list of processes involved in the algorithm as an input.

The orchestrator has methods for sending messages between the processes and acting as a channel, setting the orchestrator process used to verify the global stateand calculate the global balance.

`send_message()` method takes the sender process and receiver process and transfers the specified amount from sender to receiver. For the sake of simplicity and focusing mainly on the algorithm checks like no balance and invalid balance input are not included. However, balance underflow conditions will not impact the global balance verification check.

`set_orchestrator()` method will denote the selected process as the orchestrator that will invoke the algorithm, collect the local states and verify if the global state is consistent or not. No explicit calls for verification are required as the orchestrator process will automatically verify the global state once it recieves the local states of the participating processes.

Process colors are printed between multiple transactions to keep track of the process colors. This is done for knowing the state of the processes involved in the algorithm. These can be disabled by inserting a `'#'` before the statements.

Sample Output is shown below:

**Output:**

```
P1 has: 6000
P2 has: 6500
P3 has: 7000
P4 has: 6800
Combined Balance at start is: 26300
P1 sends 500 to P3.
P2 sends 600 to P4.
P1 sends 700 to P3.
P1 is set as orchestrator for verifying state.
Processes for verification are: ['1', '2', '3', '4']
P4 sends 900 to P2.
P1 sends 700 to P3.
Collected Local States are: {'3', '1'}
Not all local states recorded. Waiting for other local states.
Process colors are:
red white red white
P1 sends 600 to P4.
Collected Local States are: {'4', '3', '1'}
Not all local states recorded. Waiting for other local states.
Process colors are:
red white red red
3 is not neighbours with 4. Cannot send message.
Process colors are:
red white red red
P4 sends 110 to P2.
Collected Local States are: {'4', '2', '3', '1'}
Collected all Local States, Verifying Global State.
Global State is consistent
P1 has: 3500
P2 has: 6910
P3 has: 8900
P4 has: 6990
Combined Balance at end is: 26300
Process colors are:
white white white white

```