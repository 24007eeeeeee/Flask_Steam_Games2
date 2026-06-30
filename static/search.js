const optionsEls = document.querySelectorAll(".w3-card-4");
const searchEl = document.getElementById("page-search");


const search = () => 
    optionsEls.forEach(
        (e) =>
            (e.style.display =
                e.innerHTML.toUpperCase().indexOf(
                    searchEl.value.toUpperCase()
                ) > -1
                    ? ""
                    : "none")
    );

searchEl.addEventListener("input", search);