# Smart-Grid-security-simulation

Smart Grid simulation project that consists totally of four scripts, smart meter, control centre and two firewall scripts for False Data Injection and DoS detection, both with machine learning implemented.

Smart meter communicates with Utilty centre over firewalla that monitor that traffic based on packet rate and size. For more information about Smart Meter code visit my blog: https://techriot.net/index.php/2023/04/27/smart-meter-pymodbus-tcp/ 

When Firewall detects any anomaly it raises alert. Since they are using machine learnign they have to be trained on some dataset. That is why i used training.pcap which has the specific parameters, you may use another one. If you are going with training.pcap, the recommended size for testing is 5000 packets, the limit you can configure in sniff method from scapy library.

# Control Centre/Utility

Utility.py is Python script that implements a Modbus TCP server to communicate with a smart meter, which is an electronic device used for measuring electrical energy consumption. Here's a breakdown of what the script does:

The code imports the necessary modules to implement a Modbus TCP server using the pyModbusTCP library.
It defines a class called "Registers" that stores the wattage values received from the smart meter in a nested list for future processes.
The "main" function starts the Modbus TCP server and initializes two threads: "register0" and "sync_check". These threads are responsible for reading the wattage values from the smart meter and checking if the smart meter is responding or not, respectively.
The "sync_check" function runs in a while loop and checks if the smart meter has responded within the last 10 seconds. If not, it raises an alert.
The "register0" function also runs in a while loop and reads the wattage values from the smart meter by querying the holding registers and coils using the Modbus protocol. It then converts the binary data received into a float value representing the wattage, and stores it in the "mainlist" attribute of the "Registers" class. It also updates the value of the "synchronizer" variable to keep track of the latest value received from the smart meter. If the value of "recv_syncint" (the latest synchronization value) is less than the previous value of "synchronizer", it indicates that the smart meter was rebooted or there was a delay on the path, so the script raises an alert and continues to read values from the smart meter.

Overall, this script is used to monitor the energy consumption of a smart meter by reading its wattage values and storing them in a list for future processing. It also checks if the smart meter is responding in a timely manner and raises an alert if it isn't.
