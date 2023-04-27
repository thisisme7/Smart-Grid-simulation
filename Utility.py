from pyModbusTCP.server import ModbusServer
import threading, struct, time

server = ModbusServer(host="192.168.10.60", port=502, no_block=True)

class Registers:
    # wattage gets stored here for future processes
    # each list is for each thread i.e. one smart meter 
    mainlist = [[], []] 

def main():
    
    print("[+] INITIATING UTILITY [+]")
    server.start()
    try:
        threading.Thread(target=register0, daemon=False).start()
        threading.Thread(target=sync_check, daemon=False).start()
    except:
        exit()

def sync_check():
    while True:
        # Check if 10 seconds have passed without a new value received
        if time.time() - last_updated_time > 10:
            print("Alert: The SM is not responding")
            time.sleep(10)

def register0(): # Register 0 for smart meter 1
    synchronizer = 0
    global last_updated_time
    last_updated_time = time.time()
    
    while True:
        register0 = server.data_bank.get_coils(0, 32)
        recv_sync = server.data_bank.get_holding_registers(0, 1)
        recv_syncint = recv_sync[0]
        
        if recv_syncint > synchronizer:
            boolean_list = register0[:32]
            binary_string = ''.join('1' if x else '0' for x in boolean_list)
            watts = struct.unpack('f', int(binary_string, 2).to_bytes(4, byteorder='big'))[0]
            watts = round(watts, 5)
            synchronizer = recv_syncint
            Registers.mainlist[0].append(watts)
            last_updated_time = time.time()  # Reset timer on new value received
            print(watts, synchronizer)
            
        elif recv_syncint < synchronizer:
            print("SM was rebooted or there was a delay on path")
            boolean_list = register0[:32]
            binary_string = ''.join('1' if x else '0' for x in boolean_list)
            watts = struct.unpack('f', int(binary_string, 2).to_bytes(4, byteorder='big'))[0]
            watts = round(watts, 5)
            Registers.mainlist[0].append(watts)
            last_updated_time = time.time()  # Reset timer on new value received
            synchronizer = recv_syncint
            print(watts, synchronizer)
                


if __name__ == '__main__':
    main()
