import { createBoard, playMove } from "./connect4.js";

window.addEventListener("DOMContentLoaded", () => {
    const board = document.querySelector(".board");
    createBoard(board);

    const websocket = new WebSocket("ws://localhost:8001/");
    initGame(websocket);
    receiveMoves(board, websocket);
    sendMoves(board, websocket);
})

function initGame(websocket) {
    websocket.addEventListener("open", () => {
      // Send an "init" event for the first player.

      const params = new URLSearchParams(window.location.search);
      const event = { type: "init" };
      if (params.has("join")) {
        event.join = params.get("join");
      } else if (params.has("watch")) {
        event.watch = params.get("watch");
      }
      websocket.send(JSON.stringify(event));
    });
  }

function sendMoves(board, websocket) {

    const params = new URLSearchParams(window.location.search);
    if (params.has("watch")) {
        return;
    }

    board.addEventListener("click", ({ target }) => {
        const column = target.dataset.column;

        if (column === undefined) {
            return;
        }

        const event = {
            type: "play",
            column: parseInt(column, 10)
        };
        websocket.send(JSON.stringify(event));
    });
}

function showMessage(message) {
    window.setTimeout(() => window.alert(message), 50);
}

function receiveMoves(board, websocket) {
    websocket.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);
        console.log(event);
        switch (event.type) {
            case "init":
                document.querySelector(".join").href = "?join=" + event.join;
                document.querySelector(".watch").href = "?watch=" + event.watch;
                break;
            case "play":
                // Update the UI with the move.
                playMove(board, event.player, event.column, event.row);
                break;
            case "win":
                showMessage(`Player ${event.player} wins!`);
                // No further messages are expected; close the WebSocket connection.
                websocket.close(1000);
                break;
            case "error":
                showMessage(event.message);
                break;
            default:
                throw new Error(`Unsupported event type: ${event.type}.`);
        }
    });
}