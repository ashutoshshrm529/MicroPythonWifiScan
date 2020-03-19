import network
import machine
import ssd1306
import utime
import gc
gc.enable()

sda_pin = 5
scl_pin = 4

class WiFiScanner:
    def __init__(self, sda_pin, scl_pin):
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        self.name = ''
        self.strength = ''
        self.status = ''
        self.kanaal = ''
        self.i2c = machine.I2C(scl=machine.Pin(self.scl_pin), sda=machine.Pin(self.sda_pin))
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.oled.fill(1)
        self.oled.show()
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def format(self):
        try:
            wlan_list = self.wlan.scan()
        except:
            wlan_list = [['NONE', 'NONE', 'NONE', 'NONE', 'NONE', 'NONE']]
        for counter in wlan_list:
            self.name = str(counter[0], 'utf8')
            self.strength = str(counter[3]) + ' dBm'
            self.kanaal = 'Channel: ' + str(counter[2])
            self.status = self.get_secure(counter[4])
            self.show_display()
            self.oled.fill(0)
            self.oled.show()

    @staticmethod
    def get_secure(num):
        returnvalue = ""
        try:
            if int(num) == 0:
                return_value = 'Open wifi'
            elif int(num) == 1:
                return_value = 'WEP'
            elif int(num) ==2:
                return_value = 'WPA-PSK'
            elif int(num) == 3:
                return_value = 'WPA2-PSK'
            elif int(num) == 4:
                return_value = 'WPA/WPA2-PSK'
            else:
                return_value = str(num)

            return return_value
        except:
            return return_value

    def show_display(self):
        self.oled.fill(0)
        self.oled.show()
        if len(self.name) > 15:
            self.oled.text(self.name[0:15], 0, 0)
            self.oled.text(self.name[15:int(len(self.name))], 0, 8)
        else:
            self.oled.text(self.name, 0, 0)
            self.oled.text(self.strength, 30, 20)
            self.oled.text(self.status, 30, 30)
            self.oled.text(self.kanaal, 30, 40)
            self.oled.text((str(gc.mem_free()) + " B"), 30, 50)
            self.oled.show()
            utime.sleep_ms(10000)

    def __str__(self):
        return "Name: {}.\n{}\n{}.\n{}.".format(self.name, self.strength, self.kanaal, self.status)
