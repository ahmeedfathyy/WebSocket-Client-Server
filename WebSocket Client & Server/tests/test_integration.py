import pytest
import pytest_asyncio  
import asyncio
import websockets
from src.server import handler
from src.client import MathClient

# Start a server instance for testing
@pytest_asyncio.fixture  # <-- CHANGED from @pytest.fixture
async def server():
    async with websockets.serve(handler, "localhost", 8766):
        yield

@pytest.mark.asyncio
async def test_add_numbers_integration(server):
    """Test the end-to-end workflow between client and server."""
    client = MathClient(uri="ws://localhost:8766")
    
    # Test positive integer
    result = await client.call_add_numbers(10, 5)
    assert result == 15

    # Test floats
    result = await client.call_add_numbers(10.5, 0.5)
    assert result == 11.0

    # Test negative numbers
    result = await client.call_add_numbers(-5, -5)
    assert result == -10