import subprocess
import time
import thread 



def mean(arr):
    return float(sum(arr)) / len(arr)

def detectStatus():
    # checks for BAT0, BAT1 if charging, discharging or idle
    status_BAT0 = subprocess.check_output("cat /sys/class/power_supply/BAT0/status".split())
    try: status_BAT1 = subprocess.check_output("cat /sys/class/power_supply/BAT1/status".split())
    except: status_BAT1 = ""
    
    if ("Charging" in str(status_BAT0)) or ("Charging" in str(status_BAT1)):
        return 1
    if ("Discharging" in str(status_BAT0)) or ("Discharging" in str(status_BAT1)):
        return -1
    
    return 0

def getEnergyFull():
    # returns the currently installed battery capacity
    energyfull_BAT0 = subprocess.check_output("cat /sys/class/power_supply/BAT0/energy_full".split())
    energyfull_BAT0 = int(energyfull_BAT0) / 1000.

    try:
        energyfull_BAT1 = subprocess.check_output("cat /sys/class/power_supply/BAT1/energy_full".split())
        energyfull_BAT1 = int(energyfull_BAT1) / 1000.
    except: energyfull_BAT1 = 0
        
    energyfull = energyfull_BAT0 + energyfull_BAT1
    
    return energyfull

def getEnergyNow():
    # returns current remaining battery charge
    energynow_BAT0 = subprocess.check_output("cat /sys/class/power_supply/BAT0/energy_now".split())
    energynow_BAT0 = int(energynow_BAT0) / 1000.

    try:
        energynow_BAT1 = subprocess.check_output("cat /sys/class/power_supply/BAT1/energy_now".split())
        energynow_BAT1 = int(energynow_BAT1) / 1000.
    except: energynow_BAT1 = 0
    
    energynow = energynow_BAT0 + energynow_BAT1
    
    return energynow

def getPower():
    # returns current power usage
    power_BAT0 = subprocess.check_output("cat /sys/class/power_supply/BAT0/power_now".split())
    power_BAT0 = int(power_BAT0) / 1000.

    try:
        power_BAT1 = subprocess.check_output("cat /sys/class/power_supply/BAT1/power_now".split())
        power_BAT1 = int(power_BAT1) / 1000.
    except: power_BAT1 = 0
    
    power = power_BAT0 + power_BAT1
    
    return power

def battery():
    energynow = getEnergyNow() / 1000.
    energyfull = getEnergyFull() / 1000.
    status = detectStatus()
    percentage = energynow / energyfull * 100
    
    # power from mean
    powernow = power_arr[-1] / 1000.
    power = mean(power_arr) / 1000.
    
    if status > 0 and power != 0:
        tr = (energyfull - energynow) / power
        #tr = "%d:%02d" % ( int(tr), 60*(tr%1))
    elif status == -1 and power!= 0:
        tr = energynow / power
        #tr = "%d:%02d" % ( int(tr), 60*(tr%1))
    else:
        tr = None

    battery_dict = {"status": status,
                    "time": tr,
                    "power": power,
                    "powernow": powernow,
                    "energynow": energynow,
                    "energyfull": energyfull,
                    "percentage": percentage}

    return battery_dict
    
def update():
    global power_arr
    while True:
        power = getPower()
        status = detectStatus()
        global last_status
        
        if status != last_status:
            # to prevent wrong value after attaching / deattaching power cable
            power_arr = [power, power, power, power, power, power, power]
        else:
            del power_arr[0] 
            power_arr.append(power)
        
        last_status = status
        time.sleep(t)
    
    
power = getPower()
power_arr = [power, power, power, power, power, power, power]
last_status = detectStatus()

t=10 # time in between updates
thread.start_new_thread(update, () )
