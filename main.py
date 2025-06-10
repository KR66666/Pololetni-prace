import machine
import socket #pro webowi server
import dht
import time
from machine import Pin, ADC
import wlan

SSID = "iPhone"
PASSWORD = "Vojta123"
wlan.connect_wifi(SSID, PASSWORD)


dht_sensor = dht.DHT11(Pin(0))  
soil_sensor = ADC(Pin(26))      
relay = Pin(1, Pin.OUT)        #tohle je vystup na rele  

#pro čteni a načteni HTML 
def load_template():
    with open("index.html", "r") as f:
        return f.read() #vratim html

#tohle je nastaveni serveru
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
server = socket.socket()
server.bind(addr)
server.listen(1)
print("Web server running...")

while True:
    try:
        cl, addr = server.accept() #přijima připojeni
        print("Client connected from", addr)
        request = cl.recv(1024).decode() #čte http
        print("Request:", request)

        #Změříi aktuálni teplotu, vlhkost a půdní vlhkost
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        soil = soil_sensor.read_u16() #vrací hodnotu od 0 do 65535

        #automatické zalevani když je půda moc suchá
        if soil < 20000:
            relay.value(1) #zapnu čerpadlo
            time.sleep(2)
            relay.value(0)

        #ruční zalevani z webu když uživatel klikne na tlačítko
        if "POST /water" in request:
            relay.value(1)
            time.sleep(2)
            relay.value(0)

        #Načtení HTML a dosazení hodnot do šablony
        html = load_template()
        html = html.replace("{{temperature}}", str(temperature))
        html = html.replace("{{humidity}}", str(humidity))
        html = html.replace("{{soil}}", str(soil))

        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(html)
        cl.close()

    except Exception as e:
        print("Error:", e)
