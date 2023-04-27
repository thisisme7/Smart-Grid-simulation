# Smart-Grid-security-simulation
Smart Grid simulation project that consists totally of four scripts, smart meter, control centre and two firewall scripts for False Data Injection and DoS detection, both with machine learning implemented.

Smart meter communicates with Utilty centre over firewalla that monitor that traffic based on packet rate and size. For more information about Smart Meter visit my blog: https://techriot.net/index.php/2023/04/27/smart-meter-pymodbus-tcp/ 

Firewall detect any anomaly it raises alert. Since they are using machine learnign they have to be trained on some dataset. That is why i used training.pcap which has the specific parameters, you may use another one. If you are going with training.pcap, the recommended size for testing is 5000 paackets, the limit you can configure in sniff method from scapy library. 
