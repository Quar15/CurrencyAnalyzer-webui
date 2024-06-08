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
    if (changeValue > 0) {
        currencyChangePercentageTd.innerText = '+' + changeValuePercent.toFixed(3) + '%';
        currencyChangePercentageTd.classList.add("positive");
    } else if (changeValue == 0) {
        currencyChangePercentageTd.innerText = changeValuePercent.toFixed(3) + '%';
    } else {
        currencyChangePercentageTd.innerText = changeValuePercent.toFixed(3) + '%';
        currencyChangePercentageTd.classList.add("negative");
    }
    row.appendChild(currencyChangePercentageTd);

    return row;
}

function sortByKey(data, period, key) {
    return data.sort((a, b) => {
        const valueA = a[period][key];
        const valueB = b[period][key];
        
        if (typeof valueA === 'string' && typeof valueB === 'string') {
            return valueA.localeCompare(valueB);
        }
        return valueA - valueB;
    });
}

function reverseSortByKey(data, period, key) {
    return data.sort((b, a) => {
        const valueA = a[period][key];
        const valueB = b[period][key];
        
        if (typeof valueA === 'string' && typeof valueB === 'string') {
            return valueA.localeCompare(valueB);
        }
        return valueA - valueB;
    });
}

function sortTablesOnClick(e) {
    sortTableBy(e.getAttribute("sort-key"), sortByKey);
}

function reverseSortTablesOnClick(e) {
    sortTableBy(e.getAttribute("sort-key"), reverseSortByKey);
}


function swapHeaderSortOnClick(h, key) {
    sortIcon = h.querySelector("i");
    if (h.getAttribute("sort-key") === key) {
        h.classList.add("active");
        sortIcon.classList.remove("bx-sort");
        if (h.getAttribute("sort") === "desc") {
            h.setAttribute("sort", "asc");
            h.onclick = () => {
                reverseSortTablesOnClick(h);
            };
            sortIcon.classList.remove("bx-sort-down");
            sortIcon.classList.add("bx-sort-up");
        } else {
            h.setAttribute("sort", "desc");
            h.onclick = () => {
                sortTablesOnClick(h);
            };
            sortIcon.classList.remove("bx-sort-up");
            sortIcon.classList.add("bx-sort-down");
        }
    } else {
        h.classList.remove("active");
        sortIcon.classList.remove("bx-sort-up");
        sortIcon.classList.remove("bx-sort-down");
        sortIcon.classList.add("bx-sort");
        h.setAttribute("sort", "desc");
        h.onclick = () => {
            sortTablesOnClick(h);
        };
    }
}


function sortTableBy(key, sortFunction) {
    const periods = ["30days", "90days", "all", "selected"];
    for (let i = 0; i < periods.length; i++) {
        tablesDomList[i].querySelectorAll("tr:has(td)").forEach((e) => tablesDomList[i].removeChild(e));
        const sortedData = sortFunction(currencyStats, periods[i], key);
        sortedData.forEach((currencyStat) => {
            tablesDomList[i].appendChild(createRow(currencyStat, periods[i]));
        });
        let rows = tablesDomList[i].querySelectorAll("td:nth-child(1)");
        let j = 0;
        rows.forEach((r) => {
            r.style.backgroundColor = currencyColors[r.innerText];
        });
        let headers = tablesDomList[i].querySelectorAll("th");
        headers.forEach((h) => {
            swapHeaderSortOnClick(h, key);
        })
    }
}

function fillTableWithContent() {
    currencyStats.forEach((currencyStat) => {
        tablesDomList[0].appendChild(createRow(currencyStat, "30days"));
        tablesDomList[1].appendChild(createRow(currencyStat, "90days"));
        tablesDomList[2].appendChild(createRow(currencyStat, "all"));
        tablesDomList[3].appendChild(createRow(currencyStat, "selected"));
    });
}

fillTableWithContent();
currencyColors = {};
tablesDomList.forEach((table) => {
    let rows = table.querySelectorAll("td:nth-child(1)");
    let i = 0;
    rows.forEach((r) => {
        currencyColors[currencyStats[i]["all"]["currency"]] = 'rgba(' + COLORS[i] + ', .2)';
        r.style.backgroundColor = currencyColors[currencyStats[i]["all"]["currency"]];
        i++;
    })
    let headers = table.querySelectorAll("th");
    headers.forEach((h) => {
        h.setAttribute("sort", "desc");
        h.onclick = () => {
            sortTablesOnClick(h);
        };
    })
});