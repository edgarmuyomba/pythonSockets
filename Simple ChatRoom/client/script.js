window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001/");
    initChat(websocket);
    receiveMessages(websocket);
})

function initChat(websocket) {
    websocket.addEventListener("open", () => {
        const data = {
            operation: "connect",
            username: "edgarmatthew",
        }

        websocket.send(JSON.stringify(data));
    })
}

function receiveMessages(websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);

        if (event.code == 201) {
            alert("Connection Successful!")
        } else if (event.code == 205) {
            const messageContainer = document.querySelector("div.container");

            var newMessage = document.createElement("div");
            newMessage.classList.add("message");
            newMessage.classList.add("sender");

            var name = document.createElement("p");
            name.classList.add("name")
            name.textContent = event.sender;
            newMessage.appendChild(name);

            var message = document.createElement("p");
            message.classList.add("message")
            message.textContent = event.message;
            newMessage.appendChild(message);

            var time = document.createElement("p");
            time.classList.add("time")
            time.textContent = event.time;
            newMessage.appendChild(time);

            messageContainer.appendChild(newMessage);
        }
    })
}