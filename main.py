if __name__ == "__main__":
    import usb_hid
    import time
    import analogio
    import digitalio
    import math
    from board import *
    from adafruit_hid.Keyboard import Keyboard
    from adafruit_hid.Keycode import Keycode
    from adafruit_hid.consumer_control import ConsumerControl
    from adafruit_hid.consumer_control_code import ConsumerControlCode as ccc
    #usb_cdc.enable(data=True)
    dial1 = analogio.AnalogIn(A2)
    dial2 = analogio.AnalogIn(A1)
    dial3= analogio.AnalogIn(A0)
    num_dials = 3
    analogPins = [dial1, dial2, dial3]
    
    keyboard = Keyboard(usb_hid.devices)
    consumer_control = ConsumerControl(usb_hid.devices)
    button3 = digitalio.DigitalInOut(GP16)
    button3.direction = digitalio.Direction.INPUT
    button3.pull = digitalio.Pull.UP
    
    button1 = digitalio.DigitalInOut(GP15)
    button1.direction = digitalio.Direction.INPUT
    button1.pull = digitalio.Pull.UP
    
    button2 = digitalio.DigitalInOut(GP17)
    button2.direction = digitalio.Direction.INPUT
    button2.pull = digitalio.Pull.UP
    
    buttons=[
        {"button":button1, "previous_state": button1.value, "keybind": [Keycode.ALT, Keycode.F1], "type": "keyboard"},
        {"button": button2, "previous_state": button2.value, "keybind": ccc.PLAY_PAUSE, "type": "consumer_control"},
        {"button":button3, "previous_state": button3.value, "keybind": ccc.SCAN_NEXT_TRACK, "type": "consumer_control"},]
    
    dialValues = [0, 0, 0]
    
    read_interval = 0.2
    last_read_time = -1

    def setup():
        for x in range(0, num_dials):
            #set pin mode?
            pass
        
    def loop():
        updateSliderValues()
        #sendSliderValues()
        printSliderValues()



    def sendSliderValues():
        builtString = ""
        for x in range(0, num_dials):
            builtString += f'{dialValues[x]}'

            if (x < num_dials - 1):
                builtString += f'|'
        #usb_cdc.data.write(builtString.encode("ascii"))
        #print(usb_cdc.data.out_waiting)

    def updateSliderValues():
        for x in range(0,num_dials):
            dialValues[x] = math.trunc((analogPins[x].value / 64.0625610))

    def printSliderValues():
        printedString = ""
        for x in range(0, num_dials):
            printedString += f"{dialValues[x]}"


            if (x < num_dials -1):
                printedString+= "|"
            else:
                printedString+="\n"
        print(printedString)
    #previous_state = button1.value
    while True:
        now = time.monotonic()
        if now >= last_read_time + read_interval:
            loop()
            last_read_time = now
        for each in buttons:
            cur_state = each["button"].value
            if cur_state != each["previous_state"]:
                #print("button down")
                #print(button.value)
                if each["button"].value == False:
                    if each["type"] == "keyboard":
                        keyboard.press(each["keybind"][0], each["keybind"][1])
                        keyboard.release_all()
                    if each["type"] == "consumer_control":
                        consumer_control.send(each["keybind"])
            each["previous_state"] = cur_state



