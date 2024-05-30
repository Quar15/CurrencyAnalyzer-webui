var tablesDomList = document.querySelectorAll(".tables .table table tbody");

function createRow(currencyValue) {
    let row = document.createElement("tr");

    let currencyNameTd = document.createElement("td");
    currencyNameTd.innerText = currencyValue['name'];
    row.appendChild(currencyNameTd);

    let currencyHighTd = document.createElement("td");
    currencyHighTd.innerText = Math.max.apply(null, currencyValue['values']).toFixed(2) + ' PLN';
    row.appendChild(currencyHighTd);

    let currencyLowTd = document.createElement("td");
    currencyLowTd.innerText = Math.min.apply(null, currencyValue['values']).toFixed(2) + ' PLN';
    row.appendChild(currencyLowTd);

    let currencyAvgTd = document.createElement("td");
    const sum = currencyValue['values'].reduce((a, b) => a + b, 0);
    const avg = (sum / currencyValue['values'].length) || 0;
    currencyAvgTd.innerText = avg.toFixed(2) + ' PLN';
    row.appendChild(currencyAvgTd);

    let currencyChangeTd = document.createElement("td");
    const changeValue = currencyValue['values'][currencyValue['values'].length - 1] - currencyValue['values'][0];
    if (changeValue > 0) {
        currencyChangeTd.innerText = '+' + changeValue.toFixed(2) + ' PLN';
        currencyChangeTd.classList.add("positive");
    } else {
        currencyChangeTd.innerText = changeValue.toFixed(2) + ' PLN';
        currencyChangeTd.classList.add("negative");
    }
    row.appendChild(currencyChangeTd);

    let currencyChangePercentageTd = document.createElement("td");
    const changeValuePercent = (changeValue / currencyValue['values'][0]) * 100;
    if (changeValue > 0) {
        currencyChangePercentageTd.innerText = '+' + changeValuePercent.toFixed(2) + '%';
        currencyChangePercentageTd.classList.add("positive");
    } else {
        currencyChangePercentageTd.innerText = changeValuePercent.toFixed(2) + '%';
        currencyChangePercentageTd.classList.add("negative");
    }
    row.appendChild(currencyChangePercentageTd);

    return row;
}

// @TODO: Correct way to distinct 30 days, 90 days, all and from
currencyValues.forEach((currencyValue) => {
    tablesDomList.forEach((table) => {
        table.appendChild(createRow(currencyValue));
    });
});


tablesDomList.forEach((table) => {
    let rows = table.querySelectorAll("td:nth-child(1)");
    let i = 0;
    rows.forEach((r) => {
        r.style.backgroundColor = 'rgba(' + COLORS[i] + ', .2)';
        i++;
    })
});