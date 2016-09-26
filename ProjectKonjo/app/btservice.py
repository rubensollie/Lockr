from .models import BluetoothDevice
import threading
import time
import bluetooth

known_detected_devices = list()
all_detected_devices = list()

class BluetoothDetectService(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name;

    def run(self):
        global all_detected_devices
        all_detected_devices = list()

        while(True):
            try:
                nearby_devices = bluetooth.discover_devices(lookup_names=True)
                print(len(nearby_devices))

                for addr, name in nearby_devices:
                    already_added = False
                    for device in all_detected_devices:
                        if device.bluetoothaddress == addr:
                            already_added = True

                    if not already_added:
                        device = BluetoothDevice()
                        device.displayname = name
                        device.bluetoothaddress = addr
                        all_detected_devices.append(device)

                for device in all_detected_devices[:]:
                    updated = False
                    for addr, name in nearby_devices:
                        if device.bluetoothaddress == addr:
                            updated = True
                            
                    if not updated:
                        all_detected_devices.remove(device)  

            except OSError as e:
                print(e)
                pass

class BluetoothLookupService(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run (self):
        global known_detected_devices
        known_detected_devices = list()

        while(True):
            bluetooth_devices = BluetoothDevice.objects.all()

            for device in bluetooth_devices:
                try:
                    name = bluetooth.lookup_name (device.bluetoothaddress, timeout = 5)
                    if(name is not None and device not in known_detected_devices):
                        known_detected_devices.append(device)
                        print(device.bluetoothaddress + " Added")
                    elif(name is None and device in known_detected_devices):
                        known_detected_devices.remove(device)
                        print(device.bluetoothaddress + " Removed")

                except OSError as e:
                    if(device in known_detected_devices):
                        known_detected_devices.remove(device)
                        print(device.bluetoothaddress + " Removed")

                    time.sleep(5)
                    continue

                time.sleep(3)

        
