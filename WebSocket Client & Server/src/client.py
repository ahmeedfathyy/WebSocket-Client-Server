import asyncio
import websockets
import json
import logging
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - CLIENT - %(levelname)s - %(message)s"
)

class MathClient:
    def __init__(self, uri: str = "ws://localhost:8765"):
        self.uri = uri

    async def call_add_numbers(self, a: float, b: float) -> float:
        """
        Client-side function calls the server function.
        
        This function is async and returns the result when awaited. [cite: 16]
        """
        payload = {
            "action": "add",
            "params": {"a": a, "b": b}
        }

        try:
            async with websockets.connect(self.uri) as websocket:
                logging.info(f"Sending request: {payload}")
                await websocket.send(json.dumps(payload))
                
                response_raw = await websocket.recv()
                response: Dict[str, Any] = json.loads(response_raw)

                if response.get("status") == "success":
                    return response["result"]
                else:
                    error_msg = response.get("message", "Unknown error")
                    logging.error(f"Server returned error: {error_msg}")
                    raise ValueError(error_msg)

        except (OSError, websockets.exceptions.InvalidURI) as e:
            # Basic network error handling [cite: 31]
            logging.error(f"Network error connecting to {self.uri}: {e}")
            raise

async def run_demonstration():
    """
    Demonstrates calling the function multiple times with different values. [cite: 19]
    """
    client = MathClient()

    # Test Case 1: Standard addition
    try:
        val_a, val_b = 10, 20
        result = await client.call_add_numbers(val_a, val_b)
        print(f"Result of {val_a} + {val_b} = {result}") 
    except Exception as e:
        print(f"Test 1 failed: {e}")

    # Test Case 2: Floating point
    try:
        val_a, val_b = 5.5, 2.5
        result = await client.call_add_numbers(val_a, val_b)
        print(f"Result of {val_a} + {val_b} = {result}")
    except Exception as e:
        print(f"Test 2 failed: {e}")

    # Test Case 3: Error handling (simulated by passing invalid data if we had stricter types, 
    # but here we just show a successful 3rd call)
    try:
        val_a, val_b = -100, 100
        result = await client.call_add_numbers(val_a, val_b)
        print(f"Result of {val_a} + {val_b} = {result}")
    except Exception as e:
        print(f"Test 3 failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_demonstration())