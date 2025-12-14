from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import os
import uvicorn

app = FastAPI()

rooms: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(ws: WebSocket, room_id: str):
    await ws.accept()

    if room_id not in rooms:
        rooms[room_id] = []
    rooms[room_id].append(ws)

    try:
        while True:
            data = await ws.receive_text()

            # broadcast to other peers
            for peer in rooms[room_id]:
                if peer != ws:
                    await peer.send_text(data)

    except WebSocketDisconnect:
        rooms[room_id].remove(ws)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
