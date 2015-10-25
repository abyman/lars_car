#! /usr/bin/env python

import mraa
import time

LIN = 0x19
MAG = 0x1e

def connectI2C(addr=6):
   return mraa.I2c(addr)
   
class i2cDev:
   def __init__(self, bus, addr):
      self.bus = bus # handle to I2C bus
      self.addr = addr # i2c address of device on bus
   def regWrite(self,_addr,_val):
      self.bus.address(self.addr)
      self.bus.writeReg(_addr,_val)
   def readList(self,_addr,_num):
      self.bus.address(self.addr)
      _t = [-1]*_num;
      for a in range(_num):
         _t[a] = int(self.bus.readReg(_addr+a))
      return _t
         
      
def setupMag(_dev):
   dRate = 0 # 0:7 = [0.75, 1.5, 3.0, 7.5, 15, 30, 75, 220] Hz
   tEna = 1 # Enable Temp sensor
   gain = 1 # Gain setting 1100
   mode = 0 # 0:3 = [continuous, single, sleep, sleep

   # CRA_REG_M (0x00)
   _dev.regWrite(0x0, (tEna << 7 | dRate << 2))
   # CRB_REG_M (0x01)
   _dev.regWrite(0x1, gain << 5)
   # MR_REG_M (0x02)
   _dev.regWrite(0x2, mode << 0)
   return 0

def setupLin(_dev):
   # CTRL_REG1_A (0x20)
   dRate = 1 # 0:8 = [OFF, 1, 10, 25, 50, 100, 200, 400, 1620]Hz
             # 9 = 1.344 kHz (normal), 5.376kHz (low-pow mode)
   lPowMode = 0 # 1 = low power mode
   zEna = 1 # z-axis enable
   yEna = 1 # y-axis enable
   xEna = 1 # x-axis enable
   _dev.regWrite(0x20, dRate << 4 | lPowMode << 3 | zEna << 2 | yEna << 1 | xEna << 0)

   # CTRL_REG2_A (0x21)
   hPFil = 0 # 0:3 = [Normal mode, Referencs signal fir filtering, 
             #        Normal, Autoreset on interrupt]
   hPFilFc = 0 # 0:3 = [??]
   fds = 0 # filtered data selectio, 0 = filter bypassed, 1 = data from filter
   hpClick = 0 # HPF bypassed for click function
   hpis2 = 0 # HPF bypassed for AOI function on Interrupt 2
   hpis1 = 0 # HPF bypassed for AOI function on Interrupt 1
   _dev.regWrite(0x21, (hPFil << 6 | hPFilFc << 4 | fds << 3 | hpClick << 2 | \
                    hpis2 << 1 | hpis1 << 0))
 
   # CTRL_REG3_A (0x22)
   i1Click = 0 # CLICK interrupt on INT1, 0: disable, 1: enable
   i1aoi1 = 0 # AOI1 interrupt on INT1, 0: disable, 1: enable
   i1aoi2 = 0 # AOI2 interrupt on INT1, 0: disable, 1: enable
   i1drdy1 = 0 # DRDY1 interrupt on INT1, 0: disable, 1: enable
   i1drdy2 = 0 # DRDY2 interrupt on INT1, 0: disable, 1: enable
   i1wtm = 0 # FIFO watermark interrupt on INT1, 0: disable, 1: enable
   i1overrun = 0 # FIFO overrun interrupt on INT1, 0: disable, 1: enable
   _dev.regWrite(0x22, (i1Click << 7 | i1aoi1 << 6 | i1aoi2 << 5 | i1drdy1 << 4 |\
                    i1drdy2 << 3 | i1wtm << 2 | i1overrun << 1))

   # CTRL_REG4_A (0x23)
   bdu = 0 # block data update, 0: continuous update, 
           # 1: regs updated after MSB and LSB reading
   ble = 0 # big/little endian. 0: data LSB @ lower address
   fs = 0 # full scale selection 0:3 = +/- 2G, 4G, 8G, 16G
   hr = 0 # high resolution output mode, 0: low res, 1: hi res
   sim = 0 # SPI serial interface mode selection, 0: 4-wire, 1: 3-wire
   _dev.regWrite(0x23, (bdu << 7 | ble << 6 | fs << 4 | hr << 3 | sim << 0))

   # CTRL_REG5_A (0x24)
   boot = 0 # reboot memory content, 0: normal mode, 1: reboot mem content
   fifoEn = 0 # fifo enable
   lirInt1 = 0 # 1: interrupt request latched
   d4dInt1 = 0 # 4D enable on INT1
   lirInt2 = 0 # 1: interrupt request latched
   d4dInt2 = 0 # 4D enable on INT2
   _dev.regWrite(0x24, (boot << 7 | fifoEn << 6 | lirInt1 << 3 | \
                    d4dInt1 << 2 | lirInt2 << 1 | d4dInt2 << 0))

   # CTRL_REG6_A (0x25)
   i2ClickEn = 0 # click interrupt enable on PAD2
   i2Int1En = 0 # interrupt1 enable on PAD2
   i2Int2En = 0 # interrupt2 enable on PAD2
   i2Boot = 0 # reboot memory content on PAD2
   p2Act = 0 # Active function status on PAD2
   hLActive = 0 # Interrup active high
   _dev.regWrite(0x25, (i2ClickEn << 7) | (i2Int1En << 6) | (i2Int2En << 5) | \
                   (i2Boot << 4) | (p2Act << 3) | (hLActive << 1))
                   
   # REFERENCE/DATACAPTURE_A (0x26)
   Ref = 0 # Interrup active high
   _dev.regWrite(0x26, Ref)

   # FIFO_CTRL_REG_A (0x2E) 00000000
   # INT1_CFG_A      (0x30) 00000000
   # INT1_THS_A      (0x32) 00000000
   # INT1_DURATION_A (0x33) 00000000
   # INT2_CFG_A      (0x34) 00000000
   # INT2_THS_A      (0x36) 00000000
   # INT2_DURATION_A (0x37) 00000000
   # CLICK_CFG_A     (0x38) 00000000
   # CLICK_SRC_A     (0x39) 00000000
   # CLICK_THS_A     (0x3A) 00000000
   # TIME_LIMIT_A    (0x3B) 00000000
   # TIME_LATENCY_A  (0x3C) 00000000
   # TIME_WINDOW_A   (0x3D) 00000000
   
def setupPwm(_dev,hz):
   # MODE_1
   reset = 0 # writing 0 has no effect
   extclk = 0 # use internal clock
   autoInc = 0 # dont use auto-increment
   sleep = 1 # sleep to allow prescale update
   sub1 = 0 # dont respond to sub-address1
   sub2 = 0 # dont respond to sub-address3
   sub3 = 0 # dont respond to sub-address3
   allcall = 0 # dont respond to allcall
   _dev.regWrite(0x0, (reset << 7 | extclk << 6 | autoInc << 5 | sleep << 4 | sub1 << 3 
      | sub2 << 2 | sub2 << 1 | allcall))
   # PRE_SCALE
   prescale = int(round(25e6 / 4096 / hz / 0.921)) - 1
   _dev.regWrite(0xfe, prescale)
   
   sleep = 0 # wake up you lazy bum
   _dev.regWrite(0x0, (reset << 7 | extclk << 6 | autoInc << 5 | sleep << 4 | sub1 << 3 
      | sub2 << 2 | sub2 << 1 | allcall))
   # MODE 2
   invrt = 0 # output logic state not inverted
   och = 1 # 0 outputs change on stop, 1 outputs change on ACK
   outdrv = 0 # open drain config, 1 for totempole driver
   outne = 0 # see section 7.4
   _dev.regWrite(0x1, (invrt << 4 | och << 3 | outdrv << 2 | allcall))
   return (25e6/4096/prescale/0.921)
   
def adjustPwmDuty(_dev,chan,duty,phase=0,onNotOff=2):
   if(chan > 15 or chan < 0):
      return -1
   if(duty >= 1 or duty <= 0): 
      return -2
   if(phase <= -1 or phase >= 1):
      return -3
   if(onNotOff < 0 or onNotOff > 2):
      return -4
   # chan = 0:15
   _addr = (4*chan) + 6
   onBit = [0,1][onNotOff == 1]
   offBit = [0,1][onNotOff == 0]
   onCnt = (0 + int(phase*4096)) % 4096
   offCnt = (int(duty*4096) + int(phase*4096)) % 4096
   # LEDx_ON_L onCnt[7:0]
   _dev.regWrite(_addr + 0, (onCnt & 0xff))
   # LEDx_ON_H onBit + onCnt[11:8]
   _dev.regWrite(_addr + 1, onBit << 4 | ((onCnt >> 8) & 0xf))
   # LEDx_OFF_L offCnt[7:0]
   _dev.regWrite(_addr + 2, (offCnt & 0xff))
   # LEDx_ON_H onBit + onCnt[11:8]
   _dev.regWrite(_addr + 3, offBit << 4 | ((offCnt >> 8) & 0xf))
   return 0

def adjustPwmOnTime(_dev,chan,hz,ms,phase=0,onNotOff=2):
   if(chan > 15 or chan < 0):
      return -1
   if(hz <= 0 or hz >= 1500): 
      return -2
   period_ms = (float(1)/hz)*1e3
   if(float(ms) <= 0.0 or float(ms) >= period_ms): 
      return -3
   duty = ms / period_ms
   if(phase <= -1 or phase >= 1):
      return -4
   if(onNotOff < 0 or onNotOff > 2):
      return -5
   # chan = 0:15
   _addr = (4*chan) + 6
   onBit = [0,1][onNotOff == 1]
   offBit = [0,1][onNotOff == 0]
   onCnt = (0 + int(phase*4096)) % 4096
   offCnt = (int(duty*4096) + int(phase*4096)) % 4096
   # LEDx_ON_L onCnt[7:0]
   _dev.regWrite(_addr + 0, (onCnt & 0xff))
   # LEDx_ON_H onBit + onCnt[11:8]
   _dev.regWrite(_addr + 1, onBit << 4 | ((onCnt >> 8) & 0xf))
   # LEDx_OFF_L offCnt[7:0]
   _dev.regWrite(_addr + 2, (offCnt & 0xff))
   # LEDx_ON_H onBit + onCnt[11:8]
   _dev.regWrite(_addr + 3, offBit << 4 | ((offCnt >> 8) & 0xf))
   return 0














