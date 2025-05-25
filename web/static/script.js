"use strict";

const homePage = document.getElementById("home-page");
const errorPage = document.getElementById("error-page");
const loadingPage = document.getElementById("loading-page");
const resultsPage = document.getElementById("results-page");
const queryForm = document.getElementById("query-form");
const queryInput = document.getElementById("query-input");
const summary = document.getElementById("summary");
const more = document.getElementById("more");

function togglePageVisibility(page) {
    if (page.style.display === "none") {
        page.style.display = "flex";
    } else {
        page.style.display = "none";
    }
}

queryForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const query = queryInput.value;
    if (query.trim() === "") {
        alert("Please enter a search query.");
        return;
    }

    togglePageVisibility(homePage);
    togglePageVisibility(loadingPage);

    fetchResult(query);
});

function fetchResult(query) {
    fetch(`/query`
    {
        method: "POST",
            headers
    :
        {
            "Content-Type"
        :
            "application/json"
        }
    ,
        body: JSON.stringify({query: query.trim()})
    }
)
.
    then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then(data => {
            togglePageVisibility(loadingPage);
            togglePageVisibility(resultsPage);
            displayResults(data);
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
            togglePageVisibility(loadingPage);
            errorPage.innerText = error.message;
            togglePageVisibility(errorPage);
        });
}

function displayResults(data) {
    summary.innerText = data.summary || "No summary available.";
    more.innerHTML = data.more ? data.more.map(item => `<p>${item}</p>`).join("") : "No additional information available.";
}
