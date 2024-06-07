var tablesDomList = document.querySelectorAll(".tables .table table tbody");

function createRow(currencyStats, timestampKey) {
    let row = document.createElement("tr");

    let currencyNameTd = document.createElement("td");
    currencyNameTd.innerText = currencyStats[timestampKey]['currency'];
    row.appendChild(currencyNameTd);

    let currencyHighTd = document.createElement("td");
    currencyHighTd.innerText = currencyStats[timestampKey]["high"].toFixed(3) + ' PLN';
    row.appendChild(currencyHighTd);

    let currencyLowTd = document.createElement("td");
    currencyLowTd.innerText = currencyStats[timestampKey]["low"].toFixed(3) + ' PLN';
    row.appendChild(currencyLowTd);

    let currencyAvgTd = document.createElement("td");
    currencyAvgTd.innerText = currencyStats[timestampKey]["avg"].toFixed(3) + ' PLN';
    row.appendChild(currencyAvgTd);

    let currencyChangeTd = document.createElement("td");
    const changeValue = currencyStats[timestampKey]["change"];
    if (changeValue >= 0) {
        currencyChangeTd.innerText = '+' + changeValue.toFixed(3) + ' PLN';
        currencyChangeTd.classList.add("positive");
    } else {
        currencyChangeTd.innerText = changeValue.toFixed(3) + ' PLN';
        currencyChangeTd.classList.add("negative");
    }
    row.appendChild(currencyChangeTd);

    let currencyChangePercentageTd = document.createElement("td");
    const changeValuePercent = currencyStats[timestampKey]["change_perc"];
    if (changeValue >= 0) {
        currencyChangePercentageTd.innerText = '+' + changeValuePercent.toFixed(3) + '%';
        currencyChangePercentageTd.classList.add("positive");
    } else {
        currencyChangePercentageTd.innerText = changeValuePercent.toFixed(3) + '%';
        currencyChangePercentageTd.classList.add("negative");
    }
    row.appendChild(currencyChangePercentageTd);

    return row;
}

// @TODO: Correct way to distinct 30 days, 90 days, all and from
function fillTableWithContent() {
    currencyStats.forEach((currencyStat) => {
        tablesDomList[0].appendChild(createRow(currencyStat, "30days"));
        tablesDomList[1].appendChild(createRow(currencyStat, "90days"));
        tablesDomList[2].appendChild(createRow(currencyStat, "all"));
        tablesDomList[3].appendChild(createRow(currencyStat, "selected"));
    });
}
fillTableWithContent();

tablesDomList.forEach((table) => {
    let rows = table.querySelectorAll("td:nth-child(1)");
    let i = 0;
    rows.forEach((r) => {
        r.style.backgroundColor = 'rgba(' + COLORS[i] + ', .2)';
        i++;
    })
});