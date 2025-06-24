
import requests
import numpy as np
import math

def createCrossection():
    with open('capitals.csv', 'r') as capitals:
        for line in capitals:

            lat = float(line.split(',')[2])
            lon = float(line.split(',')[3])
            step = 0.005
            
            lon_init = lon

            stepInKm = step * 111.32*math.cos(math.radians(lat))
            initialCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']
            currentCountry = initialCountry
            #go east
            eastData = []
            while(currentCountry==initialCountry):
                currentCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']
                lon+=step
                elevation = round(float(requests.get('http://localhost:5000/v1/etopo1', params={'locations':str(lat)+','+str(lon)}).json()['results'][0]['elevation']),0)
                eastData.append(elevation)
            currentCountry = initialCountry
            westData = []
            lon = lon_init
            while(currentCountry==initialCountry):
                currentCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']
                lon-=step
                elevation = round(float(requests.get('http://localhost:5000/v1/etopo1', params={'locations':str(lat)+','+str(lon)}).json()['results'][0]['elevation']),0)
                westData.insert(0,elevation)
            fullList = westData+eastData
            print(len(fullList))
            dw = (stepInKm*len(westData))*-1
            de = (stepInKm*len(eastData))
            distances = np.array(np.arange(dw, de, stepInKm))
            csvFormElevation = ','.join(map(str, fullList)) 
            csvFormDistances = ','.join(map(str, distances)) 
            with open('crossection.csv', 'a', newline='') as crossection:
                crossection.write(initialCountry+','+csvFormElevation+'\n')
                crossection.write(initialCountry+','+csvFormDistances+'\n')
                crossection.close()



createCrossection()

