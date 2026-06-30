//Find all the card elements on the page that we want to show or hide when someone types in the search bar
const optionsEls = document.querySelectorAll(".w3-card-4");
// Selects the search inputs
const searchEl = document.getElementById("page-search");

// The search function code that makes it work
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
// This makes the search function every time the user inputs or clears it
searchEl.addEventListener("input", search);