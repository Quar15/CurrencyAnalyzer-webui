var graphsDom = document.querySelectorAll(".normal-chart");
var mainGraphDom = document.querySelector("#mainChart");
var graphsCharts = Array();

var maxValue = 0;

var ctxMainGraph = mainGraphDom.getContext("2d");
var mainGraphConfig = createConfig('', labels, null, 'PLN');
mainGraphConfig.data.datasets.pop();
var lineChartMainGraph = new Chart(ctxMainGraph, mainGraphConfig);

for (let i = 0; i < currencyValues.length; i++) {
    const currencyValue = currencyValues[i];
    let ctxGraph = graphsDom[i].getContext("2d");
    let config = createConfig(currencyValue['name'], labels, currencyValue['values'], 'PLN');
    config.data.datasets[0] = {
        label: currencyValue['name'],
        backgroundColor: 'rgba(' + COLORS[i] + ', 0.2)',
        borderColor: 'rgba(' + COLORS[i] + ', 1)',
        fill: true,
        borderWidth: 3,
        data: currencyValue['values'],
    }
    let lineChart = new Chart(ctxGraph, config);
    graphsCharts.push(lineChart);
    addDataset(lineChartMainGraph, {
        label: currencyValue['name'],
        backgroundColor: 'rgba(' + COLORS[i] + ', 0.2)',
        borderColor: 'rgba(' + COLORS[i] + ', 1)',
        fill: true,
        borderWidth: 3,
        data: currencyValue['values'],  
    });

    chartMaxValue = Math.max.apply(null, currencyValue['values']);
    if (chartMaxValue > maxValue) {
        maxValue = chartMaxValue;
    }
}

graphsCharts.forEach((chart)=> {
    addLineToChart(chart, 'transparent', maxValue);
})

updateFilterList();