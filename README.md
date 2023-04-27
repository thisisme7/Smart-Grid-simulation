# Smart-Grid-security-simulation
Smart Grid simulation project that consists totally of four scripts, smart meter, control centre and two firewall scripts for False Data Injection and DoS detection, both with machine learning implemented.

Smart meter communicates with Utilty centre over firewalla that monitor that traffic based on packet rate and size. If it does detect any anomaly it raises alert. Sincce they are using machine learnign they have to be trained on some datasets. That is why i used training.pcap which has the specifyc parameters, you may use another one. 
