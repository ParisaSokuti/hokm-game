# client.py
import asyncio
import websockets
import json

SERVER_URI = "ws://localhost:8765"

async def main():
    print("Welcome to Hokm!")
    username = input("Enter your username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    has_room = input("Do you have a room code? (y/n): ").strip().lower()
    if has_room == 'y':
        room_code = input("Enter the 4-character room code: ").strip().upper()
        if len(room_code) != 4:
            print("Room code must be 4 characters.")
            return
        action = "join_room"
    else:
        room_code = None
        action = "create_room"

    try:
        async with websockets.connect(SERVER_URI) as ws:
            # Send join/create message
            msg = {
                "type": action,
                "username": username,
            }
            if room_code:
                msg["room_code"] = room_code
            await ws.send(json.dumps(msg))

            while True:
                try:
                    msg = await ws.recv()
                    data = json.loads(msg)
                    if data.get('type') == 'room_joined':
                        print(f"Player {data['player_number']}: {username} entered the room [{data['room_id']}]")
                        print(f"Players in room: {data['total_players']}/4")
                        if data['total_players'] == 4:
                            print("Room is full, ready to play!")
                    elif data.get('type') == 'error':
                        print("Error:", data.get('message'))
                        break
                    elif data.get('type') == 'game_start':
                        print("Game is starting!")
                    else:
                        print("Server:", data)
                except websockets.ConnectionClosed:
                    print("Connection closed by server.")
                    break
    except KeyboardInterrupt:
        print("\nClient exited.")

if __name__ == "__main__":
    asyncio.run(main())
