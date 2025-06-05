from mcp.client.sse import sse_client
from mcp import ClientSession

def get_client(url="http://localhost:8000/sse"):
    return sse_client(url)
