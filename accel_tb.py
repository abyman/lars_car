#! /usr/bin/env python

import time
import accel

# Connect to I2C bus
i2cHandle = accel.connectI2C(6)
# create handle to magField I2C slave
magField = accel.i2cDev(i2cHandle,0x1e)
# create handle to linAccel I2C slave
linAccel = accel.i2cDev(i2cHandle,0x19)
# create handle to pwm I2C slave
pwm = accel.i2cDev(i2cHandle,0x40)

# Setup Mag and Lin devices
accel.setupMag(magField)
accel.setupLin(linAccel)
PWM_HZ = accel.setupPwm(pwm,50.0)
if 0:
   for a in range(0,10,1):
      ttt = magField.readList(0x31,2)
      t = ttt[0] << 4 | ttt[1] >> 4
      if t >= 2**11:
         t = t - 2**12
      t = float(t) / 8.0

      xzy = magField.readList(0x3,6)
      x = xzy[0] << 8 | xzy[1]
      if x >= 2**15:
         x = x - 2**16
      z = xzy[2] << 8 | xzy[3]
      if z >= 2**15:
         z = z - 2**16
      y = xzy[4] << 8 | xzy[5]
      if y >= 2**15:
         y = y - 2**16
      #x = magField.reverseByteOrder(magField.readU16(0x3))
      #y = magField.reverseByteOrder(magField.readU16(0x7))
      #z = magField.reverseByteOrder(magField.readU16(0x5))
      print "%s %s %s %s" % (t, x, y, z)

      a = linAccel.readList(0x28,1)
      b = linAccel.readList(0x29,1)
      c = linAccel.readList(0x28,2)
      print "  %s %s %s" % (a,b,c)
      #time.sleep(1)

      
s = 2.4 - (2.4-0.5)/2
accel.adjustPwmOnTime(pwm,15,PWM_HZ,s,0.4)
print "middle?"
#Stime.sleep(3)
sp = 0.1
accel.adjustPwmDuty(pwm,0,sp,0.0,0)
accel.adjustPwmDuty(pwm,1,sp,0.0,2)

while sp > -1.0 and sp < 1.0:
   if sp > 0:
      accel.adjustPwmDuty(pwm,0,sp,0.0,2)
      accel.adjustPwmDuty(pwm,1,sp,0.0,0)
   elif sp < 0:
      accel.adjustPwmDuty(pwm,0,abs(sp),0.0,0)
      accel.adjustPwmDuty(pwm,1,abs(sp),0.0,2)
   else:
      accel.adjustPwmDuty(pwm,0,0.5,0.0,1)
      accel.adjustPwmDuty(pwm,1,0.5,0.0,1)
   sp = input("Enter Speed: ")
accel.adjustPwmDuty(pwm,0,0.5,0.0,1)
accel.adjustPwmDuty(pwm,1,0.5,0.0,1)
      

incr = 0.05
while 0:
   accel.adjustPwmOnTime(pwm,15,PWM_HZ,s,0.4)
   print s
   if s >= 2.4:
      incr = -incr
   if s <= 0.5:
      incr = -incr
   s = s + incr
   time.sleep(0.1)
s = 0.5
while 0:
   accel.adjustPwmOnTime(pwm,15,PWM_HZ,s,0.4)
   print s
   if s == 2.4:
      s = 0.5
   elif s == 0.5:
      s = 2.4
   time.sleep(1)
   