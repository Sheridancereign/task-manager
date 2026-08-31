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

document.body.addEventListener("htmx:responseError", (event) => {
    console.log("HTMX response error caught:", event.detail.xhr.status);
    if (event.detail.xhr.status === 400) {
        alert("Please check the form — some fields are invalid.");
    }
});