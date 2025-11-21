# WebSocket Client & Server Exercise

This package implements a WebSocket server that performs calculations and a client that requests them.


Environment Setup

1. **Prerequisites:** Python 3.10+
2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

websockets>=12.0
#This is the main library used to create the server and client connections.
pytest>=8.0
#This is the testing framework needed to run the automated tests mentioned in the "Optional / Bonus Tasks"
pytest-asyncio>=0.23
#Since the functions must be async, this specific plugin allows pytest to test asynchronous code correctly.

## Example Output
Enter two numbers (e.g., '10 20'): 10 20 
Result: 30.0

Enter two numbers (e.g., '10 20'): 10 Mobiles
Invalid input. Please enter numbers only.
...
