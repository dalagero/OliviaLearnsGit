import os
import usbtmc
import time
from usb.core import find as finddev

'''Establish communications with RIGOL Oscilloscope via USB and make it record dataframes, then play through them while recording them to numbered txt files. Set for infinite data recording.
Roberto Mandujano 2018'''

# Initialize device
instr = usbtmc.Instrument(0x1ab1, 0x04b1)
print(instr.ask("*IDN?"))
m=1
while 1==1:
	#Start Recording
	instr.write("FUNC:WRM REC")
	instr.write("FUNC:WREC:OPER REC")
        time.sleep(2400)

	# Setup scope for reading
	instr.write("WAV:SOUR CHAN1")
	instr.write(":WAV:MODE NORM")
	instr.write(":WAV:FORM ASC")

	# Get setup data (hscale, vscale, hstep, vstep, #oftraces, etc) from scope
	timeinc = instr.ask(":WAV:XINC?")
	energyinc = instr.ask(":WAV:YINC?")

	# open file for writing data and write header
	#file = open("muon.txt","w")
	#file.write(timeinc + "\n")
	#file.write(energyinc + "\n")
	print(instr.ask(":FUNC:WREC:FMAX?"))
	print(instr.ask(":FUNC:WREP:FCUR?"))

	muondecays = instr.ask(":FUNC:WREP:FCUR?")
	file = open("muonrun" + str(m),"w")

	for n in range(1, int(muondecays)):
		instr.write("WAV:SOUR CHAN1")
		instr.write(":WAV:MODE NORM")
		instr.write(":WAV:FORM ASC")
		instr.write(":FUNC:WREP:FCUR "+str(n))
		data = instr.ask(":WAV:DATA?")
		time.sleep(.01)
		file.write(data + "\n")
		time.sleep(.01)

	file.close()
        m = m+1



