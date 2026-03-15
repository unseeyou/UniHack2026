const timeElements = document.querySelectorAll("time");
for (const timeEl of timeElements) {
    const time = timeEl.dateTime;
    const dateTime = new Date(time);

    dateTime.setTime(dateTime.getTime() - new Date().getTimezoneOffset() * 60000);

    if (timeEl.hasAttribute("dateonly")) {
        timeEl.textContent = dateTime.toLocaleDateString();
    }
    else if (timeEl.hasAttribute("timeonly")) {
        timeEl.textContent = dateTime.toLocaleTimeString();
    }
    else {
        timeEl.textContent = dateTime.toLocaleString();
    }
}