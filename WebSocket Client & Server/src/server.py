import asyncio
import websockets
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - SERVER - %(levelname)s - %(message)s"
)

def add_numbers(a: float, b: float) -> float:
    """
    Server function that adds two numbers.
    
    Args:
        a (float): First number.
        b (float): Second number.

    Returns:
        float: The sum of a and b.
    """
    return a + b

async def handler(websocket):
    """
    Handles incoming WebSocket connections and processes RPC-style requests.
    """
    client_id = str(websocket.id)
    logging.info(f"Client connected: {client_id}")

    try:
        async for message in websocket:
            try:
                data: Dict[str, Any] = json.loads(message)
                logging.info(f"Received request from {client_id}: {data}")

                # protocol: {"action": "add", "params": {"a": 1, "b": 2}}
                action = data.get("action")
                params = data.get("params", {})

                if action == "add":
                    # Validate inputs
                    if not all(k in params for k in ("a", "b")):
                        raise ValueError("Missing parameters 'a' or 'b'")
                    
                    # Perform computation [cite: 12]
                    result = add_numbers(params["a"], params["b"])
                    
                    response = {"status": "success", "result": result}
                else:
                    response = {"status": "error", "message": f"Unknown action: {action}"}

            except json.JSONDecodeError:
                response = {"status": "error", "message": "Invalid JSON format"}
            except ValueError as e:
                response = {"status": "error", "message": str(e)}
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                response = {"status": "error", "message": "Internal server error"}

            # Send response back to client
            await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        logging.info(f"Client disconnected: {client_id}")

async def main():
    # Start the server on localhost:8765
    async with websockets.serve(handler, "localhost", 8765):
        logging.info("Server started on ws://localhost:8765")
        await asyncio.get_running_loop().create_future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")