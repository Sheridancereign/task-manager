document.body.addEventListener("htmx:configRequest", (event) => {
    event.detail.headers["X-CSRFToken"] = getCookie("csrftoken");
});

function getCookie(name) {
    const cookieValue = document.cookie
        .split("; ")
        .find((row) => row.startsWith(name + "="))
        ?.split("=")[1];
    return cookieValue;
}