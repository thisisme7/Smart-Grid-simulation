from pyModbusTCP.client import ModbusClient
import random, threading, time, subprocess, struct

######################################
##### Smart Meter Modbus client
######################################

class Data:
    
    def __init__(self):    
        self.kettle = 0
        self.tv = 0
        self.fridge = 0

    def background_collect(self):
        try:
            while True:
                # watt hours simulation
                self.kettle = abs(random.uniform(0.0300, 0.0700) + self.kettle) 
                self.tv = abs(random.uniform(0.0100, 0.0300) + self.tv) 
                self.fridge = abs(random.uniform(0.0100, 0.0200) + self.fridge)
                time.sleep(1) # to save computation power of CPU
        except Exception:
            print("Energy collection stopped")
            exit()
            


def sendData(collector):
    client = ModbusClient(host="10.0.0.1", auto_open=True, auto_close=False, port=502)
    
    while True:
        try:
            client.open()
            if client.open() == True:
                print("[+] MOBUS SESSION OPENED [+]")
                synchronizer = 1
                while client.open():
                    
                    watts = collector.kettle + collector.tv + collector.fridge
                    watts = round(watts, 5)
                    print(watts)
                    
                    float_bytes = struct.pack('f', watts)
                    binary_string = ''.join(f'{byte:08b}' for byte in float_bytes)
                    boolean_list = [bit == '1' for bit in binary_string]
                    client.write_multiple_coils(0, boolean_list)
                    client.write_single_register(0, synchronizer)
                    synchronizer += 1
                    
                    collector.kettle = 0
                    collector.tv = 0
                    collector.fridge = 0
                    time.sleep(5)

        except Exception as e:
            print("[+] MODBUS SESSION FAILED [+]")
            print(e)


def collect(collector):
    try:
        threading.Thread(target=collector.background_collect, daemon=True).start()
        print("[+]DATA COLLECTOR STARTED[+]")
    except:
        print("[+]DATA COLLECTOR FAILED[+]")


def ipsec():
    try:
        subprocess.run(["swanctl", "--load-all"])
        subprocess.run(["swanctl", "--initiate", "--child", "host-host"])
        if subprocess.run(["swanctl", "--initiate", "--child", "host-host"]).returncode == 0:
            print("[+] IPsec ESTABLISHED [+]")
            menu(sec_session=True)
        else:
            raise Exception
    except KeyboardInterrupt:
        print("Establishment interrupted")
    except Exception:
        print("Establishment failed")

######################################
##### Main menu initiators
######################################

def menu(sec_session=bool):
    while True:
        print()
        print("[+]-- SMART METER MENU --[+]")
        print("1. Start collecting data")
        print("2. Secure connection")
        print("3. Start sending data")
        
        try:
            option = input("your choice: ")
            option = int(option)
            if option == 1:
                threading.Thread(target=collect, args=(collector,)).start()
            elif option == 2:
                ipsec()
            elif option == 3 and sec_session == True:
                sendData(collector=collector)
            else:
                print("Ipsec is not established")
        except ValueError:
            print("Not an integer")
        except KeyboardInterrupt:
            exit()
        except Exception as exc:
            print(exc)
    
    
if __name__ == '__main__':
    collector = Data()
    time.sleep(1)
    menu()
