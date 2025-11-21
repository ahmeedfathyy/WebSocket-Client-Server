import asyncio
import websockets
import json
import logging
from typing import Dict, Any
from enum import IntEnum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - SERVER - %(levelname)s - %(message)s"
)

class HTTPStatus(IntEnum):
    """HTTP-style status codes"""
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

def addNumbers(firstNumber: float, secondNumber: float) -> float:
    """
    Adds two numbers and returns the result.
    
    Args:
        firstNumber: The first numeric operand
        secondNumber: The second numeric operand
    
    Returns:
        The sum of firstNumber and secondNumber
    """
    return firstNumber + secondNumber

async def handleWebSocketConnection(websocket):
    """
    Handles incoming WebSocket connections from clients.
    
    Maintains a persistent connection that processes multiple requests
    from the same client using an async for loop.
    
    Args:
        websocket: The WebSocket connection object
    """
    # Generate a unique identifier for the client
    if hasattr(websocket, 'remote_address') and websocket.remote_address:
        clientIdentifier = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    else:
        clientIdentifier = f"conn-{id(websocket)}"
    
    logging.info(f"Client connected: {clientIdentifier}")

    try:
        # Process incoming messages continuously
        # This loop keeps the connection open for multiple requests
        async for messageData in websocket:
            responsePayload = {}
            try:
                requestData: Dict[str, Any] = json.loads(messageData)
                logging.info(f"Request received from {clientIdentifier}: {requestData}")

                requestAction = requestData.get("action")
                requestParameters = requestData.get("params", {})

                if requestAction == "add":
                    # Validate that required parameters exist
                    if not all(key in requestParameters for key in ("a", "b")):
                        responsePayload = {
                            "status": "error",
                            "status_code": HTTPStatus.BAD_REQUEST,
                            "message": "Missing required parameters 'a' or 'b'"
                        }
                    # Validate parameter types
                    elif not all(isinstance(requestParameters[key], (int, float)) for key in ("a", "b")):
                        responsePayload = {
                            "status": "error",
                            "status_code": HTTPStatus.BAD_REQUEST,
                            "message": "Parameters 'a' and 'b' must be numeric"
                        }
                    # Execute the addition operation
                    else:
                        calculationResult = addNumbers(requestParameters["a"], requestParameters["b"])
                        responsePayload = {
                            "status": "success",
                            "status_code": HTTPStatus.OK,
                            "result": calculationResult
                        }
                        logging.info(f"Computed: {requestParameters['a']} + {requestParameters['b']} = {calculationResult}")

                else:
                    responsePayload = {
                        "status": "error",
                        "status_code": HTTPStatus.NOT_FOUND,
                        "message": f"Unknown action: '{requestAction}'"
                    }

            except json.JSONDecodeError:
                responsePayload = {
                    "status": "error",
                    "status_code": HTTPStatus.BAD_REQUEST,
                    "message": "Invalid JSON format"
                }
            except Exception as e:
                logging.error(f"Unexpected error: {e}", exc_info=True)
                responsePayload = {
                    "status": "error",
                    "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
                    "message": "Internal server error"
                }

            # Send the response back to the client
            await websocket.send(json.dumps(responsePayload))

    except websockets.exceptions.ConnectionClosed:
        # Connection closed normally by the client
        logging.info(f"Client disconnected: {clientIdentifier}")
    except Exception as e:
        logging.error(f"Fatal connection error: {e}")

async def startServer():
    """
    Initializes and starts the WebSocket server.
    
    The server listens on localhost:8765 and maintains persistent
    connections with clients using periodic ping messages.
    """
    serverHost = "localhost"
    serverPort = 8765
    pingIntervalSeconds = 20
    
    async with websockets.serve(handleWebSocketConnection, serverHost, serverPort, ping_interval=pingIntervalSeconds):
        logging.info(f"Server started on ws://{serverHost}:{serverPort}")
        # Keep the server running indefinitely
        await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(startServer())
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")