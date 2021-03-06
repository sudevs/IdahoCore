import sys

try:
    from serial import Serial
except:
    from fakes import Serial
    print("pySerial package NOT FOUND")


SOM = b'\x7E'
EOM = b'\xE7'
SC =  b'\x00'
    
LABEL_OUTPUT_ONLY_SEND_DMX = b'\x06'


class Widget:
    """Class to interface with the USBDMX Pro Widget"""
        
    def __init__(self, port):
        try:
            if(port == 'fake'):
                import fakes
                self.serialPort = fakes.Serial(port='/dev/fake')
            else:
                self.serialPort = Serial(port=port, baudrate=57600, timeout=1)
            print("Connected to USBDMX on port '%s'" % (self.serialPort.portstr))
        except:
            print("ERROR: Could not open port '%s'" % port)
            sys.exit(1)
    
    def transmit(self, label, data):
        data_size = len(data)
        header = bytearray(label)
        header.append(int(data_size & 0xFF))
        header.append(int((data_size >> 8) & 0xFF)) 
        message = SOM + header + data + EOM
        self.serialPort.write(message)
    
    def send_dmx(self, packet):
        msg = SC + bytes(packet.data)
        self.transmit(LABEL_OUTPUT_ONLY_SEND_DMX, msg)

    def send_palette(self, palette):
        self.send_dmx(Packet(palette))

class Packet:
    def __init__(self, colors):
        self.data = bytearray()
        for color in colors:
            r, g, b = color
            self.data.append(int(g * 255))
            self.data.append(int(r * 255))
            self.data.append(int(b * 255))

def rotate(l,n):
    return l[n:] + l[:n]

if __name__ == "__main__":
    widget = Widget('/dev/ttyUSB0')
    import color
    import time
    #Ex 1: Spread a rainbow across all the strands
    numStrands=4
    palette = color.rainbow_palette(numStrands, 1.0, 1.0)
    widget.send_dmx(Packet(palette))

    #Ex 2: Fade the first strand through the color spectrum in steps of 52
    #palette = color.rainbow_palette(52, 1.0, 1.0)
    #i = 0
    #while True:
        #i = (i+1) % 52
        #widget.send_dmx(Packet([palette[i],palette[i],palette[i],palette[i]]))
        # time.sleep(.05)
