import serial
from serial.tools import list_ports


class SerialInterface:
    """ Class to interconnect kivy GUI with Arduino board 
        using serial communication.
    """
    def __init__(self):
        self.serial_port = None

    def get_ports(self):
        self.serial_ports = list_ports.comports()
        return self.serial_ports

    def get_port_names(self):
        available_ports = self.get_ports()
        return [name for name, _, _, in available_ports]

    def connect_port(self, port_name, baud_rate=9600):
        """ Connects to a port with a given name. """
        try:
            self.serial_port = serial.Serial(port_name, baud_rate, timeout=0)
        except serial.serialutil.SerialException as e:
            print(e)
        return self.serial_port

    def connect_to_plant(self, plant_id):
        """ connects Grid, solar or battery from the plant .
            Args:
                plant_id: id of a plant. 'g' for grid
                's' for solar and 'b' for battery
        """
        if self.serial_port:
            command = plant_id + '1'
            self.serial_port.write(bytes(command, 'ascii'))
            return True
        else:
            return False

    def disconnect_from_plant(self, plant_id):
        """ disconnects Grid, solar, or battery.
              Args:
                plant_id: id of a plant. 'g' for grid
                's' for solar and 'b' for battery
        """
        if self.serial_port:
            command = plant_id + '0'
            self.serial_port.write(bytes(command, 'ascii'))
            return True
        else:
            return False

    def connect_grid(self):
        """ connects load Grid. """
        if self.serial_port:
            self.serial_port.write(b'g1')
            return True
        else:
            return False

    def disconnect_grid(self):
        """ disconnects load from Grid. """
        if self.serial_port:
            self.serial_port.write(b'g0')
            return True
        else:
            return False

    def connect_battery(self):
        """ connects battery from solar pannel. """
        try:
            self.serial_port.write(b'b1')
            return True
        except serial.serialutil.SerialException as e:
            print(e)
        return False

    def disconnect_battery(self):
        """ disconnects battery from solar pannel. """
        try:
            self.serial_port.write(b'b0')
            return True
        except serial.serialutil.SerialException as e:
            print(e)
        return False


# testing the library:
if __name__ == '__main__':
    ports = SerialInterface().get_port_names()
    for port in ports:
        print(port)