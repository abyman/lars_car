#! /usr/bin/env python

import time
import accel
import string

SERVO_LEFT = 2.4
SERVO_RIGHT = 0.5

# Connect to I2C bus
i2cHandle = accel.connectI2C(6)
# create handle to magField I2C slave
magField = accel.i2cDev(i2cHandle,0x1e)
# create handle to linAccel I2C slave
linAccel = accel.i2cDev(i2cHandle,0x19)
# create handle to pwm I2C slave
pwm = accel.i2cDev(i2cHandle,0x40)

# Setup Mag and Lin and PWM devices
accel.setupMag(magField)
accel.setupLin(linAccel)
PWM_HZ = accel.setupPwm(pwm,50.0)

def setMotorSpeed(sp,pwm,pwmPair=[0,1]):
   if sp == 1:
      accel.adjustPwmDuty(pwm,pwmPair[0],0.5,0.0,1)
      accel.adjustPwmDuty(pwm,pwmPair[1],0.5,0.0,0)
   if sp == -1:
      accel.adjustPwmDuty(pwm,pwmPair[0],0.5,0.0,0)
      accel.adjustPwmDuty(pwm,pwmPair[1],0.5,0.0,1)
   elif sp > 0:
      accel.adjustPwmDuty(pwm,pwmPair[0],sp,0.0,2)
      accel.adjustPwmDuty(pwm,pwmPair[1],sp,0.0,0)
   elif sp < 0:
      accel.adjustPwmDuty(pwm,pwmPair[0],abs(sp),0.0,0)
      accel.adjustPwmDuty(pwm,pwmPair[1],abs(sp),0.0,2)
   else:
      accel.adjustPwmDuty(pwm,pwmPair[0],0.5,0.0,1)
      accel.adjustPwmDuty(pwm,pwmPair[1],0.5,0.0,1)

def setServoAngle(s,pwm,pwmNum=15):
   sp = ((SERVO_LEFT+SERVO_RIGHT)/2) + s*(SERVO_LEFT-SERVO_RIGHT)/2
   accel.adjustPwmOnTime(pwm,pwmNum,PWM_HZ,sp,0.4)
   
def usage():
   print("Enter one of the following commands with associated parameter")
   print(" a <speed> // motor a will turn at speed. speed is (-1:1)")
   print(" b <speed> // motor b will turn at speed. speed is (-1:1)")
   print(" c <speed> // motor a&b will turn at speed. speed is (-1:1)")
   print(" s <pos> // servo s will turn to pos. pos is (-1:1)")
   print(" exit // exit this prog")

s = 0
setServoAngle(s,pwm)
setMotorSpeed(0,pwm,[0,1])      
setMotorSpeed(0,pwm,[2,3])      

run = 1
while run:
   raw = raw_input("% ")
   if len(raw) == 0:
      usage()
   else:
      spl = string.split(string.lower(raw))
      if spl[0] == 'a' or spl[0] == 'b' or spl[0] == 'c' or spl[0] == 's':
         if len(spl) < 2:
            usage()
         else:
            v = float(spl[1])
            if v < -1 or v > 1:
               usage()
            else:
               if spl[0] == 'a' or spl[0] == 'c':
                  setMotorSpeed(v,pwm,[0,1])
               if spl[0] == 'b' or spl[0] == 'c':
                  setMotorSpeed(v,pwm,[2,3])
               if spl[0] == 's':
                  setServoAngle(v,pwm)
      elif spl[0] == 'exit':
         run = 0
      else:
         usage()
      