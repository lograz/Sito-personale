// script.js

document.addEventListener("DOMContentLoaded", () => {
    // Simulate an API request or any async operation
    setTimeout(() => {
        hideLoader();
        showContent();
    }, 1000); // Replace with your actual data loading logic and time

    function hideLoader() {
        const loader = document.getElementById("loader");
        document.getElementById("loader").classList.add("loaderani")

    }

    function showContent() {
        const content = document.getElementById("content");
        content.style.display = "flex";
    }
});

