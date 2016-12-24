
import ultrasonic

def run_test():
	# substitute your pins here
	u = ultrasonic.Ultrasonic(4, 5)

	# the default MicroPython build doesn't have functools (for reduce), so I keep a running count of valid
	# runs and a sum...
 
	sum = 0
	valid = 0
	for i in range(0, 1000):
		d = u.distance_in_cm()
		if d > 0:
			sum += d
			valid += 1	
		else:
			print("error ", d, " at run ", i, " ", valid, " have succeeded so far...")

	return(valid, sum / valid)	

