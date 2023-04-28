# Smart-Grid-security-simulation

Smart Grid simulation project that consists totally of four scripts, smart meter, control centre and two firewall scripts for False Data Injection and DoS detection, both with machine learning implemented.

# Smart meter 

Smart Meter communicates with Utilty centre over firewall that monitor that traffic based on packet rate and size. For more information about Smart Meter code visit my blog: https://techriot.net/index.php/2023/04/27/smart-meter-modbus-tcp/ 

# Control Centre/Utility

Utility.py is Python script that implements a Modbus TCP server to communicate with a smart meter, which is an electronic device used for measuring simulation of electrical energy consumption. Description is on my blog as well: https://techriot.net/index.php/2023/04/28/control-centre/

# False Data Injection detection

# Denial of Service detection

Program tains itself on dataset using one-class SVM model based on packet frequency and then determines if the captured amount of packets exceeds the trained rate. IF yes, program raises alert but with some modification can take an action.Description is on my blog: https://techriot.net/index.php/2023/04/28/firewall-denial-of-service-ids/
