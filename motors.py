#! /usr/bin/env python

import time
import accel
import string
import sys



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
   
def setLightIntensity(sp,pwm,pwmNum=8):
   if sp <= 1 and sp >= 0:
      accel.adjustPwmDuty(pwm,pwmNum,sp,0.0)
   
def usage():
   print("Enter one of the following commands with associated parameter")
   print(" a <speed> // motor a will turn at speed. speed is (-1:1)")
   print(" b <speed> // motor b will turn at speed. speed is (-1:1)")
   print(" c <speed> // motor a&b will turn at speed. speed is (-1:1)")
   print(" s <pos> // servo s will turn to pos. pos is (-1:1)")
   print(" t <delay> // servo s will turn right and then left. each step will be delayed by delay")
   print(" l <num> <intensity> // light <num (1:2)> on with <intensity (0:1)>")
   print(" exit // exit this prog")

s = 0
setServoAngle(s,pwm)
setMotorSpeed(0,pwm,[0,1])      
setMotorSpeed(0,pwm,[2,3])      
setLightIntensity(0.015,pwm,12)
setLightIntensity(0.015,pwm,13)

if len(sys.argv) > 1:
   spl = sys.argv[1:]
   if spl[0] == 'a' or spl[0] == 'b' or spl[0] == 'c' or spl[0] == 's' or spl[0] == 't' or spl[0] == 'l':
      if len(spl) < 2:
         usage()
      else:
         if len(spl) > 2:
            v = float(spl[2])
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
            if spl[0] == 't':
               for a in range(0,17,1):
                  setServoAngle(a*0.01,pwm)
                  time.sleep(v)
               for a in range(16,-17,-1):
                  setServoAngle(a*0.01,pwm)
                  time.sleep(v)
               for a in range(-16,1,1):
                  setServoAngle(a*0.01,pwm)
                  time.sleep(v)
            if spl[0] == 'l':
               setLightIntensity(v,pwm,int(spl[1])+11)
               print "%s, %s" % (v, int(spl[1]))
   elif spl[0] == 'exit':
      run = 0
   else:
      usage()
else:
   run = 1
   while run:
      raw = raw_input("% ")
      if len(raw) == 0:
         usage()
      else:
         spl = string.split(string.lower(raw))
         if spl[0] == 'a' or spl[0] == 'b' or spl[0] == 'c' or spl[0] == 's' or spl[0] == 't' or spl[0] == 'l':
            if len(spl) < 2:
               usage()
            else:
               if len(spl) > 2:
                  v = float(spl[2])
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
                  if spl[0] == 't':
                     for a in range(0,17,1):
                        setServoAngle(a*0.01,pwm)
                        time.sleep(v)
                     for a in range(16,-17,-1):
                        setServoAngle(a*0.01,pwm)
                        time.sleep(v)
                     for a in range(-16,1,1):
                        setServoAngle(a*0.01,pwm)
                        time.sleep(v)
                  if spl[0] == 'l':
                     setLightIntensity(v,pwm,int(spl[1])+7)
         elif spl[0] == 'exit':
            run = 0
         else:
            usage()
         