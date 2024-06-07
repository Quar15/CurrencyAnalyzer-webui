searchBar = document.querySelector("#currency-search");
tableRecords = document.querySelectorAll("td:nth-child(2)");
if (searchBar) {
    searchBar.addEventListener("keyup", () => {
        let searchContent = searchBar.value.toLowerCase();
        let re = new RegExp(".*" + searchContent + ".*");
        tableRecords.forEach(e => {
            if (! e.innerText.toLowerCase().match(re)) {
                e.parentElement.classList.add("unfiltered");
            } else {
                e.parentElement.classList.remove("unfiltered");
            }
        });
    });
}