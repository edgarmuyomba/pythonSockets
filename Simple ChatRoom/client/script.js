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

        switch (event.code) {
            case 201:
                alert("Connection Successful!")
                break;
            case 202:
                // add an online user
                const users = document.querySelector("div.users");
                users.innerHTML = `
                    <div class="header">
                        <p class="title">Users</p>
                        <p class="subtitle">Currently Online</p>
                    </div>
                `;

                const online_users = event.data;

                for (const user of online_users) {
                    var newUser = document.createElement("div");
                    newUser.classList.add("user");
                    newUser.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                            <title>account</title>
                            <path
                            d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
                        </svg>
                        <p class="name">${user} </p><span class="active"></span>
                    `;

                    users.appendChild(newUser);
                }

                break;
            case 205:
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
                break;
        }
    })
}