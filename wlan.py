import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(20):  
        if wlan.isconnected():
            print("Connected to Wi-Fi")
            print(wlan.ifconfig())
            return True
        time.sleep(0.5)
    
    print("Failed to connect to Wi-Fi")
    return False
