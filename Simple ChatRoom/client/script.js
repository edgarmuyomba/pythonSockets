window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001/");

    websocket.addEventListener("open", () => {
        getUsername(websocket);
    })
})

function getUsername(websocket) {
    const username_form = document.querySelector("form#username_form");
    var username = "";
    username_form.addEventListener("submit", (event) => {
        event.preventDefault();
        var username_field = username_form.querySelector("input#username");
        username = username_field.value;
        username_field.value = "";
        registerUser(websocket, username);
    });
}

function registerUser(websocket, username) {
    // get the username and attempt to register

    const data = {
        operation: "connect",
        username: username,
    }

    websocket.send(JSON.stringify(data));

    websocket.addEventListener("message", function onMessage({ data }) {
        const response = JSON.parse(data);

        if (response.code == 200) {
            // success
            const welcomeScreen = document.querySelector("div.welcome");
            const messageScreen = document.querySelector("div.messages");

            welcomeScreen.style.display = "none";
            messageScreen.style.display = "block";
            websocket.removeEventListener("message", onMessage);
            receiveMessages(websocket);
            sendMessages(websocket);
        } else {
            // failed
            alert(response.message);
        }
    })

}

function receiveMessages(websocket) {
    websocket.addEventListener("message", ({ data }) => {

        const response = JSON.parse(data);

        switch (response.code) {
            case 201:
                alert("Connection Successful!");
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

                const online_users = response.data;

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
                name.textContent = response.sender;
                newMessage.appendChild(name);

                var message = document.createElement("p");
                message.classList.add("message")
                message.textContent = response.message;
                newMessage.appendChild(message);

                var time = document.createElement("p");
                time.classList.add("time")
                time.textContent = response.time;
                newMessage.appendChild(time);

                messageContainer.appendChild(newMessage);
                break;
        }
    })
}

function sendMessages(websocket) {
    const message_form = document.querySelector("form#message");
    const message_field = message_form.querySelector("input#message");
    message_form.addEventListener("submit", () => {
        const message = message_field.value;
        message_field.value = "";
        const data = {
            operation: "receive",
            sender: username,
            message: message
        };
        websocket.send(JSON.stringify(data));
    })
}