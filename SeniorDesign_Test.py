from SeniorDesign_IRcam import pyIRcam
from time import sleep,time
from Tkinter import *

update_rate = 20 # 20ms update rate

camera = pyIRcam() # Sensor initialization


master = Tk()
w = Canvas(master, width = 1024, height =768) #IR Camera Dimensions
w.pack(fill = BOTH, expand = 1)

def update_Image():
    camera.getPositions() #Update with new IR objects
    w.delete(ALL)
    if camera.positions['found']:
        camera.findTarget()
    if(camera.targetFound):
        color = "blue"
    else:
        color ="red"
        w.create_rectangle(camera.positions['1'][0], camera.positions['1'][1], camera.positions['1'][0] + 10, camera.positions['1'][1] + 10, fill = color)
        w.create_rectangle(camera.positions['2'][0], camera.positions['2'][1], camera.positions['2'][0] + 10, camera.positions['2'][1] + 10, fill = color)
        w.create_rectangle(camera.positions['3'][0], camera.positions['3'][1], camera.positions['3'][0] + 10, camera.positions['3'][1] + 10, fill = color)
        w.create_rectangle(camera.positions['4'][0], camera.positions['4'][1], camera.positions['4'][0] + 10, camera.positions['4'][1] + 10, fill = color)

master.after(0, update_Image)
master.mainloop()



"""while True:
    current = time() # Counters for loop
    elapsed = 0

    camera.getPositions() # Update found IR objects 

    if camera.positions['found']: # If an IR object is found, print the information
        print (("Object 1: %d, %d | Object 2: %d, %d | Object 3: %d, %d | Object 4: %d, %d") % (camera.positions['1'][0],camera.positions['1'][1],camera.positions['2'][0],camera.positions['2'][1],camera.positions['3'][0],camera.positions['3'][1],camera.positions['4'][0],camera.positions['4'][1]))

    while elapsed < update_rate:
        elapsed = time() - current # Wait until the loop completes, perfect update_rate loop"""

