import machine, time, onewire, ds18x20, socket
# the device is on GPIO12
dat = machine.Pin(12)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
roms = ds.scan()

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Temperatures</title> </head>
    <body style="background-color: #aaaaaa; font-size: 22px;"> <h1 style="">ESP8266 Temperatures</h1>
        <table border="1"> <tr><th>Sensor</th><th>Temperature</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    ds.convert_temp()
    time.sleep_ms(750)
    rows = ['<tr><td>%s</td><td>%f</td></tr>' % (str(rom), ds.read_temp(rom) for rom in roms]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
