const BACKGROUND_COLOR = "rgba(99, 255, 132, 0.2)";
const BORDER_COLOR = "rgb(99, 255, 132)";
const CROSSHAIR_COLOR = "rgb(99, 255, 132)";
const GRID_COLOR = "rgba(99, 255, 132, 0.1)";

const COLORS = [
    "99, 255, 132",
    "132, 99, 255",
    "255, 132, 99",
    "39, 219, 242",
    "255, 99, 132",
    "219, 242, 39",
];

function padNum(num, size) {
    num = num.toString();
    while (num.length < size) num = "0" + num;
    return num;
}

function formatDate(date) {
    let datePart = [
        date.getFullYear(),
        date.getMonth() + 1,
        date.getDate(),
    ].map((n, i) => n.toString().padStart(i === 4 ? 4 : 2, "0")).join("-");
    return datePart;
  }

function addLineToChart(chart, color, value) {
    if (!chart.config.options.plugins.annotation) {
        chart.config.options.plugins.annotation = { annotations: [] };
    }

    chart.config.options.plugins.annotation.annotations.push({
        type: 'line',
        mode: 'horizontal',
        scaleID: 'y',
        value: value,
        borderColor: color,
        borderWidth: 2,
    });

    chart.update();
}

function addVerticalLineToChart(chart, color, value) {
    if (!chart.config.options.plugins.annotation) {
        chart.config.options.plugins.annotation = { annotations: [] };
    }

    chart.config.options.plugins.annotation.annotations.push({
        type: 'line',
        mode: 'vertical',
        scaleID: 'x',
        value: value,
        borderColor: color,
        borderWidth: 2,
    });

    chart.update();
}

function addData(chart, newData, datasetIndex = -1) {
    if (datasetIndex >= 0) {
        chart.data.datasets[datasetIndex].data.push(newData);
    } else {
        chart.data.datasets.forEach((dataset) => {
            dataset.data.push(newData);
        });
    }
    chart.update();
}

function addDataset(chart, dataset) {
    chart.config.data.datasets.push(dataset);
    chart.update();
}

function removeData(chart) {
    chart.data.labels.shift();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.shift();
    });
    chart.update();
}

const afterDate = (timestamp, value) => { 
    let today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    today.setMilliseconds(0);
    let todayTimestamp = today.getTime();
    return timestamp >= todayTimestamp ? value : [];
};
function createConfig(labelText, dataLabels, dataValues, yAxisUnit = '%') {
    return {
        type: "line",
        data: {
            labels: dataLabels,
            datasets: [
                {
                    label: labelText,
                    data: dataValues,
                    fill: true,
                    backgroundColor: BACKGROUND_COLOR,
                    borderColor: BORDER_COLOR,
                    lineTension: 0.01,
                }
            ],
        },
        options: {
            borderDash: (ctx) => afterDate(Date.parse(labels[labels.length - 1]), [5, 5]),
            hover: {
                intersect: false,
            },
            interaction: {
                intersect: false,
                mode: 'nearest',
                axis: 'x'
            },
            indexAxis: "x",
            responsive: false, // Use specified width and height
            scales: {
                y: {
                    ticks: {
                        callback: function(value, index, values) {
                            return value.toFixed(2) + ' ' + yAxisUnit;
                        }
                    },
                    grid: {
                        color: GRID_COLOR,
                    },
                    border: {
                        display: false,
                        dash: [5, 5],
                    },
                },
                x: {
                    grid: {
                        display: false,
                        lineWidth: 0,
                    },
                    border: {
                        dash: [5, 5]
                    },
                    type: 'time',
                    time: {
                        unit: "day",
                        displayFormats: {
                            day: 'yyyy-MM-dd'
                        }
                    },
                    offsetAfterAutoskip: true,
                    ticks: {
                        source: 'labels',
                        minRotation: 45
                    },
                }
            },
            segment:{
                borderDash: (ctx) => afterDate(ctx.p0.parsed.x, [5, 5])
            },
            plugins: {
                tooltip: {
                    mode: "interpolate",
                    intersect: false,
                    animation: false,
                },
                crosshair: {
                    line: {
                        color: CROSSHAIR_COLOR,
                    },
                    snap: {
                        enabled: true
                    },
                    sync: {
                        enabled: true,
                        group: 1,
                        suppressTooltips: false,
                    },
                    zoom: {
                        enabled: false
                    }
                },
            },
        },
    };
}

function updateNavFocus(buttonIndex) {
    navLinks = document.querySelectorAll("nav a");
    navLinksMap = {}
    navLinks.forEach((a) => {
        a.classList.remove("active");
        navLinksMap[a.innerText.toLowerCase().split(' (')[0]] = a;
    });
    navLinksMap[buttonIndex].classList.add("active");
}

function updateFilterList() {
    filterListLinks = document.querySelectorAll("#filter-list a");
    timeframes = [7, 28, 84, 168, 365];
    for(let i=0; i < timeframes.length; i++) {
        let days = timeframes[i];
        let ms = new Date(Date.now() - days*24*60*60*1000);
        filterListLinks[i].setAttribute("hx-vals", '{"since": "' + formatDate(ms) + '"}');
    }
}

function getInputVal(id) {
    el = document.querySelector("#" + id);
    return el.value;
}

function hideOnClick(selector) {
    let elements = document.querySelectorAll(selector);
    elements.forEach((e) => {
        e.addEventListener('click', ()=> {
            e.classList.add("hidden");
        })
    });
}

function colorChangeColumns(tablesDomList, rowsSelector = 'td:nth-child(5), td:nth-child(6)') {
    tablesDomList.forEach((table) => {
        let rows = table.querySelectorAll(rowsSelector);
        rows.forEach((r) => {
            let value = parseFloat(r.innerText);
            if (!isNaN(value) && value > 0) {
                r.classList.add("positive");
            } else {
                r.classList.add("negative");
            }
        })
    });
}
