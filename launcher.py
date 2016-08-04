import time
import os
import sys
import usb.core

class Launcher(): # a parent class for our low level missile launchers.  
#Contains general movement commands which may be overwritten in case of hardware specific tweaks.
            
    # roughly centers the turret at the origin
    def center(self, x_origin=0.5, y_origin=0.5):
        print 'Centering camera ...'
        self.moveToPosition(x_origin,y_origin)

    def moveToPosition(self, right_percentage, down_percentage): 
        self.turretLeft()
        time.sleep( self.x_range)
        self.turretRight()
        time.sleep( right_percentage * self.x_range)
        self.turretStop()

        self.turretUp()
        time.sleep( self.y_range)
        self.turretDown()
        time.sleep( down_percentage * self.y_range) 
        self.turretStop()

    def moveRelative(self, right_percentage, down_percentage):
        if (right_percentage>0):
            self.turretRight()
        elif(right_percentage<0):
            self.turretLeft()
        time.sleep( abs(right_percentage) * self.x_range)
        self.turretStop()
        if (down_percentage>0):
            self.turretDown()
        elif(down_percentage<0):
            self.turretUp()
        time.sleep( abs(down_percentage) * self.y_range)
        self.turretStop()



# Launcher commands for DreamCheeky Thunder (VendorID:0x2123 ProductID:0x1010)
class Launcher2123(Launcher):
    # Low level launcher driver commands
    # this code mostly taken from https://github.com/nmilford/stormLauncher
    # with bits from https://github.com/codedance/Retaliation
    def __init__(self):
        self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)

        # HID detach for Linux systems...tested with 0x2123 product

        if self.dev is None:
            raise ValueError('Missile launcher not found.')
        if sys.platform == "linux2":
            try:
                if self.dev.is_kernel_driver_active(1) is True:
                    self.dev.detach_kernel_driver(1)
                else:
                    self.dev.detach_kernel_driver(0)
            except Exception, e:
                pass

        #some physical constraints of our rocket launcher
        self.missile_capacity = 4
        #experimentally estimated speed scaling factors 
        self.y_speed = 0.48
        self.x_speed = 1.2    
        #approximate number of seconds of movement to reach end of range  
        self.x_range = 6.5  # this turret has a 270 degree range of motion and if this value is set
                            # correcly should center to be facing directly away from the usb cable on the back
        self.y_range = 0.75

        #define directional constants        
        self.DOWN = 0x01
        self.UP = 0x02
        self.LEFT = 0x04
        self.RIGHT = 0x08

    def __del__(self):
        self.turretStop()
        self.ledOff()

    def turretUp(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretDown(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretLeft(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretRight(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretDirection(self,direction):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, direction, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretStop(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turretFire(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def ledOn(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    def ledOff(self):
        self.dev.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
