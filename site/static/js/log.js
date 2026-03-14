const logElement = document.getElementById("logs");

const oldLog = console.log;
console.log = (...data) => {
    oldLog(...data);

    const logChild = document.createElement("p");
    logChild.classList.add("card-text")
    logChild.innerText = data.map(JSON.stringify).join(" ");
    logElement.appendChild(logChild);
}

const oldError = console.error;
console.error = (...data) => {
    oldError(...data);

    const logChild = document.createElement("p");
    logChild.style = "color: red";
    logChild.classList.add("card-text")
    logChild.innerText = data.map(JSON.stringify).join(" ");
    logElement.appendChild(logChild);
}

document.addEventListener("error", e => {
    console.error(e.error);
});
