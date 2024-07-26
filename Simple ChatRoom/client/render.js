function renderSenderMessage(data) {
    const messageContainer = document.querySelector("div.container");

    var newMessage = document.createElement("div");
    newMessage.classList.add("message");
    newMessage.classList.add("sender");

    var name = document.createElement("p");
    name.classList.add("name")
    name.textContent = data.sender;
    newMessage.appendChild(name);

    var message = document.createElement("p");
    message.classList.add("message")
    message.textContent = data.message;
    newMessage.appendChild(message);

    var time = document.createElement("p");
    time.classList.add("time")
    time.textContent = data.time;
    newMessage.appendChild(time);

    messageContainer.appendChild(newMessage);
}

function renderSentMessage(data) {
    const messageContainer = document.querySelector("div.container");

    var newMessage = document.createElement("div");
    newMessage.classList.add("message");
    newMessage.classList.add("recipient");

    var message = document.createElement("p");
    message.classList.add("message")
    message.textContent = data.message;
    newMessage.appendChild(message);

    var time = document.createElement("p");
    time.classList.add("time")
    time.textContent = data.time;
    newMessage.appendChild(time);

    messageContainer.appendChild(newMessage);
}

export { renderSenderMessage, renderSentMessage }