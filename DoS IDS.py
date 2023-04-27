from scapy.all import IP, rdpcap, sniff
from sklearn.svm import OneClassSVM
from decimal import Decimal
import numpy as np


# Loading training dataset
print("LOADING DATASET...")
valid = rdpcap('datasets/training.pcap') # packets with valid two-way traffic

# function to extract the packet rate for loaded dataset
def packet_rate(dataset):
    times = [packet.time for packet in dataset]
    return Decimal(len(times)) / Decimal(times[-1] - times[0])

def captured_packets(captured_set):
    # Group the packets by source IP address
    packets_by_srcip = {}
    for packet in captured_set:
        srcip = packet[IP].src
        if srcip not in packets_by_srcip:
            packets_by_srcip[srcip] = []
        packets_by_srcip[srcip].append(packet)

    # Compute the packet rate for each group of packets
    packet_rates = []
    for srcip, packets in packets_by_srcip.items():
        times = [packet.time for packet in packets]
        packet_rates.append(Decimal(len(times)) / Decimal(times[-1] - times[0]))

    # Compute the average packet rate for all groups
    return np.mean(packet_rates)

# Compute the packet rate for the loaded dataset
valid_rate = packet_rate(valid)

# Train the one-class SVM model 
model = OneClassSVM(kernel='rbf', nu=0.1, gamma=0.1)
model.fit(np.array([[float(valid_rate)]]))

# Start monitoring
print("MONITORING START...")
try:
    while True:
        captured_traffic = sniff(count=5000) # size of traffic for analysis

        # Compute the packet rate for the captured dataset
        print("ANALYSIS START...")
        capt_rate = captured_packets(captured_traffic)
        # Determine the threshold for a DoS attack
        threshold = float(valid_rate * Decimal(1.5))

        # Predict whether the captured traffic is an outlier (i.e., potential DoS attack)
        is_outlier = model.predict(np.array([[float(capt_rate)]]))[0] == -1

        # Calculate the probability of a DoS attack based on the similarity to the training data
        if capt_rate > threshold and is_outlier:
            prob = min(100, ((capt_rate - valid_rate) / valid_rate) * 100)
        else: 
            prob = 0 
            
        print(f"Probability of DoS attack {prob:.2f}%")
        print("capt rate: ", capt_rate)
        

except KeyboardInterrupt:
    print("Quitting the program")
    exit()
except Exception:
    print(Exception)
