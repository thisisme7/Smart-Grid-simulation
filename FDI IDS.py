from scapy.all import *
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy

# Load dataset and extract features
print("LOADING DATASET...")
dataset = rdpcap('datasets/training.pcap')
packetsizes = []
for packet in dataset:
    packetsizes.append(len(packet))

# Calculate mean and standard deviation of packet sizes in dataset
mean_packetsize = numpy.mean(packetsizes)
std_packetsize = numpy.std(packetsizes)

# Define the IsolationForest model and the scaler for packet size normalization
isolationforest = IsolationForest(n_estimators=100, contamination=0.05)
scaler = StandardScaler()

# Train the scaler and fit the IsolationForest model on dataset
scaler.fit(numpy.array(packetsizes).reshape(-1, 1))
isolationforest.fit(scaler.transform(numpy.array(packetsizes).reshape(-1, 1)))


def traffic_process(traffic):
    global mean_packetsize, std_packetsize, isolationforest, scaler
    # Extract packet sizes from network traffic
    traffic_packetsizes = []
    for packet in traffic:
        packet_size = len(packet)
        traffic_packetsizes.append(packet_size)
        # exclude the unauthorized protocols
        if packet.haslayer(TCP) and not packet.haslayer(ESP) and not packet.haslayer(ISAKMP):
            print("ALERT: unauthorized protocol")

    # Calculate the mean packet size of the captured network traffic
    mean_traffic_packetsize = numpy.mean(traffic_packetsizes)
    
    # If the mean packet size of captured network traffic 
    # is significantly higher than that of dataset, print alert
    if mean_traffic_packetsize > mean_packetsize + 2*std_packetsize:
        print("ALERT: anomaly detected")
    else:
        print("Packet size OK")
    
    print("Valid average packet size: ", mean_packetsize)
    print("Captured average packet size:", mean_traffic_packetsize)


print("STARTING MONITORING...")
while True:
    capt_traff = sniff(count=5000)
    time.sleep(2)
