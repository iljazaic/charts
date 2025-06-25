
import requests
import numpy as np
import math

def createCrossection():
    with open('capitals.csv', 'r') as capitals:
        try:
            for line in capitals:
                try:
                    lat = round(float(line.split(',')[2]),5)
                    lon = round(float(line.split(',')[3]),5)
                    step = 0.001

                    lon_init = lon

                    unknown_tolerancy = 5000
                    current_unknown = 0
                    stepInKm = step * 111.32*math.cos(math.radians(lat))
                    initialCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']
                    currentCountry = initialCountry
                    #go east
                    eastData = []
                    while(currentCountry==initialCountry or current_unknown<=unknown_tolerancy and currentCountry=='Unknown'):
                        lon+=step

                        currentCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']
                        if currentCountry=='Unknown' or current_unknown>0 and currentCountry!=initialCountry:
                            current_unknown+=1
                        else:
                            current_unknown=0
                        elevation = round(float(requests.get('http://localhost:5000/v1/etopo1', params={'locations':str(lat)+','+str(lon)}).json()['results'][0]['elevation']),0)
                        eastData.append(elevation)
                    currentCountry = initialCountry
                    if current_unknown>0:
                        del eastData[-current_unknown:]
                    current_unknown=0
                    step=0.001
                    westData = []
                    lon = lon_init

                    while(currentCountry==initialCountry or current_unknown<=unknown_tolerancy and currentCountry=='Unknown'):
                        lon-=step
                        currentCountry = requests.get('http://localhost:5000/countryAtCoord', params={'lat':lat,'lon':lon}).json()['country']

                        if currentCountry=='Unknown' or current_unknown>0 and currentCountry!=initialCountry:
                            current_unknown+=1
                        else:
                            current_unknown=0

                        elevation = round(float(requests.get('http://localhost:5000/v1/etopo1', params={'locations':str(lat)+','+str(lon)}).json()['results'][0]['elevation']),0)
                        westData.insert(0,elevation)

                    if current_unknown>0:
                        westData=westData[current_unknown:]

                    fullList = westData+eastData
                    dw = (stepInKm*len(westData))*-1
                    de = (stepInKm*len(eastData))
                    distances = np.array(np.arange(dw, de, stepInKm))
                    csvFormElevation = ','.join(map(str, fullList)) 
                    csvFormDistances = ','.join(map(str, distances)) 
                    with open('crossection3.csv', 'a', newline='') as crossection:
                        crossection.write(initialCountry+','+csvFormElevation+'\n')
                        crossection.write(initialCountry+','+csvFormDistances+'\n')
                        crossection.close()
                except:
                    print(line.split(',')[0])
        except:
            print('oh no')
createCrossection()

