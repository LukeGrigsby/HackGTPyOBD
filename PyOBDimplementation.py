import obd
import time
import csv


class SpeedandEfficiency():
    def _init_(self, speed, efficiency):
        self.speed = speed
        self.efficiency = efficiency
SEList = []
maxSE = SpeedandEfficiency(0.0,0.0)
num_loaded = 0
num_new = 0
#Records data for speed efficiency calculations
def EfficiencyButtonRecord():
    valueRecorded = False
    fuelRateTotal = 0
    speedTotal = 0
    fuelRateCounter = 0
    speedCounter = 0
    minSpeed = 0
    maxSpeed = 0
    def new_spd(obdqueryrefer) :
        speedquery = obdqueryrefer.value.magnitude
        if speedQuery < minSpeed : minSpeed = speedQuery
        if speedQuery > maxSpeed : maxSpeed = speedQuery
        speedTotal += speedquery
        speedCounter += 1
    def new_fr(obdqueryrefer) :
        fuelratequery = obdqueryrefer.value.magnitude
        fuelRateTotal += fuelratequery
        fuelRateCounter += 1
    connectionfr = obd.Async()
    connections = obd.Async()
    connectionfr.watch(obd.commands.FUEL_RATE, callback=new_fr)
    connections.watch(obd.commands.SPEED, callback=new_spd)
    connectionfr.start()
    connections.start()
    t_end = time.time() + 10
    while time.time() < t_end:
        pass
    connectionfr.stop()
    connections.stop()
    speedAverage = (SpeedTotal/speedCounter)
    averageConsumption = (fuelRateTotal/fuelRateCounter)/speedAverage #liters per mile
    if ((maxSpeed - minSpeed) < 3) :
        addValue = SpeedandEfficiency(speedAverage, averageConsumption)
        SEList.append(addValue)
        valueRecorded = True
    return valueRecorded
#keep track of num_loaded for exit func
def StartupSEList(num_loaded_):
    with open("PyOBDFuelEconomy.csv", newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter = ',')
        line_count = 0
        for row in filereader :
            if(line_count == 0) :
                line_count += 1
            elif(line_count == 1) :
                maxSE.speed = float(row[0])
                maxSE.efficiency = float(row[1])
                line_count += 1
            else :
                SEList.append(SpeedandEfficiency(float(row[0]),float(row[1])))
                num_loaded_ += 1
                line_count += 1
    return num_loaded_
def ExitSEList(num_new_):
    with open("PyOBDFuelEconomy.csv", 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in range(num_new_) :
            filewriter.writerow([SEList[num_loaded + x].speed, SEList[num_loaded + x].efficiency])
#pass a SpeedandEfficiency object
#have to manually update MaxSE this only returns the new max
#is this how python for loops work?
def UpdateEMax(currentMax):
    for ele in SEList :
        if ele.efficiency < currentMax.efficiency :
            currentMax = SEList[i]
    return currentMax
def speedVector():
    speedvector = []
    i = 0
    while i < len(SEList) :
       speedvector.append(float(SEList[i].speed))
       i += 1
    return speedvector
def effVector():
    effvector = []
    i = 0
    while i < len(SEList) :
        effvector.append(float(SEList[i].efficiency))
        i += 1
    return effvector
#current list format
#SPEED,EFFICIENCY //Format marker
#CURRENT,MAX // max efficiency point
#DATA,POINTS // list of all efficiency points
