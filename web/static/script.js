"use strict";

const homePage = document.getElementById("home-page");
const errorPage = document.getElementById("error-page");
const loadingPage = document.getElementById("loading-page");
const resultsPage = document.getElementById("results-page");
const queryForm = document.getElementById("query-form");
const queryInput = document.getElementById("query-input");
const queryString = document.getElementById("query-string");
const summary = document.getElementById("summary");
const more = document.getElementById("more");
const errorMessage = document.getElementById("error-message");
const resultsSplash = document.getElementById("results-splash");

window.onload = function () {
    queryForm.reset();
};

function togglePageVisibility(page) {
    if (page.style.display === "none" || page.style.display === "") {
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
    fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query: query.trim()})
        }
    ).then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then(data => {
            displayResults(data);
            togglePageVisibility(loadingPage);
            togglePageVisibility(resultsPage);
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
            errorMessage.innerText = error.message;
            togglePageVisibility(loadingPage);
            togglePageVisibility(errorPage);
        });
}

function displayResults(data) {
    summary.innerText = data.summary || "No summary available.";
    more.innerHTML = data.more || "No additional information available.";
    queryString.innerText = `Query: ${queryInput.value || "No query provided."}`;
    resultsSplash.style.backgroundColor = interpolateColor(data.certainty);
}

function interpolateColor(multiplier) {
    // Green: (0,255,0), Red: (255,0,0)
    const r = Math.round(255 * multiplier);
    const g = Math.round(255 * (1 - multiplier));
    const b = 0;
    return `rgba(${r},${g},${b},0.6)`;
}
