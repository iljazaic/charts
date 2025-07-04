const { count } = require('console');
const express = require('express');
const fs = require('fs')
const path = require('path')
const app = express();

app.use(express.static(__dirname.replace('server', 'public')));

async function compileCrossectionData(country) {
    const data = fs.readFileSync('./topography/crossection3.csv', 'utf-8');
    const lines = data.split('\n');
    var package = {
        'Distances': [],
        'Elevations': []
    }
    for (let i = 0; i < lines.length; i++) {
        const countryLine = lines[i].split(',')[0];
        if (country == countryLine || country.toLowerCase() == countryLine.toLowerCase() || countryLine.toLowerCase().includes(country.toLowerCase())) {
            const elevationData = lines[i].split(',');
            var distanceData = lines[i + 1].split(',');
            elevationData.shift();
            distanceData.shift();

            for (let j = 0; j < distanceData.length; j++) {
                let d = Math.round(parseFloat(distanceData[j]));
                if (d <= 0) {
                    distanceData[j] = d.toString() + 'km-W'
                } else {
                    distanceData[j] = d.toString() + 'km-E'
                }
            }
            package.Distances = distanceData;
            package.Elevations = elevationData;
            return package;
        }
    }

}


async function compileDietData(country) {
    const data = fs.readFileSync('./server/datasets/OurWorldInData/dietaryData.csv', 'utf-8');
    const lines = data.split('\n');

    var package = [];
    const valueArray = lines[0].split(',')
    for (let i = 0; i < lines.length; i++) {
        const countryLine = lines[i].split(',')[0];
        if (country == countryLine || country.toLowerCase() == countryLine.toLowerCase() || countryLine.toLowerCase().includes(country.toLowerCase())) {
            const dietData = lines[i].split(',');
            for (let j = 2; j < dietData.length; j++) {
                package.push({ name: valueArray[j]+': '+dietData[j]+'kCal', value: parseFloat(dietData[j]), itemStyle:{color:{image:'./images/diet/'+valueArray[j]+'.png', repeat:'repeat'}} })
            }
            return package;
        }
    }

}

async function getNewDataset(country) {
    return 'diet'
}


app.get("/getNewDataset", async (req, res) => {
    const country = req.query.c;

    //template to send back?
    const package = {
        'chartType': '',
        'data': []
    }

    const chartType = await getNewDataset(country);

    package.chartType = chartType;

    switch (chartType) {
        case 'crossection':
            package.data = await compileCrossectionData(country);
            break;
        case 'diet':
            package.data = await compileDietData(country);
    }
    res.send(package);
})

app.get("/", async (req, res) => {
    res.sendFile('C:/Users/iljaz/desktop/charts_game/public/index.html')
})

app.listen(3000, () => {
    console.log("user connected");
})
