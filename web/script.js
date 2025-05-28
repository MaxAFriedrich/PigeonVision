"use strict";

const homePage = document.getElementById("home-page");
const errorPage = document.getElementById("error-page");
const loadingPage = document.getElementById("loading-page");
const resultsPage = document.getElementById("results-page");
const pigeonPage = document.getElementById("pigeon-page");
const queryForm = document.getElementById("query-form");
const queryInput = document.getElementById("query-input");
const queryString = document.getElementById("query-string");
const summary = document.getElementById("summary");
const more = document.getElementById("more");
const errorMessage = document.getElementById("error-message");
const resultsSplash = document.getElementById("results-splash");

let jobId = null;
let jobCheckInterval = null;

const domain = window.location.hostname;

window.onload = function () {
    queryForm.reset();
    window.scrollTo(0, 0);
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

    if (query.trim()=== domain){
        togglePageVisibility(homePage);
        togglePageVisibility(pigeonPage);
        return;
    }

    if (DEV === true) {
        togglePageVisibility(homePage);
        togglePageVisibility(loadingPage);
        fetchResult(query, "test-token");
        return;
    }

    turnstile.ready(function () {
        turnstile.render("#turnstile", {
            sitekey: SITEKEY,
            callback: function (token) {
                togglePageVisibility(homePage);
                togglePageVisibility(loadingPage);

                fetchResult(query, token);
            },
        });
    });

});

function checkJobStatus() {
    fetch(`/job/${jobId}`).then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    }).then(response => {
        if (response.ok) {
            const data = response.result;
            displayResults(data);
            togglePageVisibility(loadingPage);
            togglePageVisibility(resultsPage);
            clearInterval(jobCheckInterval);
        }
    });
}

function fetchResult(query, token) {
    fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query: query.trim(), token: token})
        }
    ).then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
        .then(data => {
            jobId = data.id;
            jobCheckInterval = setInterval(checkJobStatus, 1000);
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
