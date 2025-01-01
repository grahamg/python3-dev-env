import pytest
import requests

# This is a naive example that calls the running container's endpoint
# In practice, you might want a more isolated testing approach.
def test_index():
    # Assuming the container is running on localhost:8003
    resp = requests.get("http://localhost:8003/")
    assert resp.status_code == 200
    assert "Todo List" in resp.text
