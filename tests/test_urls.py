from fastapi.testclient import TestClient

def test_create_short_url_random_code(client: TestClient):
    """Test generating a short URL with a random 6-character code."""
    payload = {
        "target_url": "https://example.com/some/long/path",
        "custom_alias": None,
        "expires_in_days": None
    }
    response = client.post("/api/v1/shorten", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["target_url"] == "https://example.com/some/long/path"
    assert len(data["short_code"]) == 6
    assert data["is_active"] is True
    assert "short_url" in data

def test_create_short_url_custom_alias(client: TestClient):
    """Test creating a short URL with a custom alias."""
    payload = {
        "target_url": "https://fastapi.tiangolo.com/",
        "custom_alias": "fastapi",
        "expires_in_days": 10
    }
    response = client.post("/api/v1/shorten", json=payload)
    assert response.status_code == 201
    assert response.json()["short_code"] == "fastapi"

def test_duplicate_custom_alias_fails(client: TestClient):
    """Test that creating a duplicate custom alias returns HTTP 400."""
    payload = {
        "target_url": "https://google.com",
        "custom_alias": "myalias"
    }
    # First creation should succeed
    res1 = client.post("/api/v1/shorten", json=payload)
    assert res1.status_code == 201

    # Second creation with identical alias must fail
    res2 = client.post("/api/v1/shorten", json=payload)
    assert res2.status_code == 400
    assert "already in use" in res2.json()["detail"]

def test_invalid_url_fails_validation(client: TestClient):
    """Test that malformed URLs are rejected with HTTP 422."""
    payload = {
        "target_url": "not-a-valid-url"
    }
    response = client.post("/api/v1/shorten", json=payload)
    assert response.status_code == 422

def test_redirect_to_target_url(client: TestClient):
    """Test that accessing /{short_code} redirects with HTTP 302."""
    payload = {
        "target_url": "https://python.org/",
        "custom_alias": "pyorg"
    }
    client.post("/api/v1/shorten", json=payload)

    response = client.get("/pyorg", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "https://python.org/"


def test_nonexistent_url_returns_404(client: TestClient):
    """Test that requesting a missing short code returns HTTP 404."""
    response = client.get("/nonexistent123", follow_redirects=False)
    assert response.status_code == 404

def test_url_stats_and_soft_delete(client: TestClient):
    """Test statistics retrieval and soft deletion lifecycle."""
    client.post("/api/v1/shorten", json={"target_url": "https://github.com", "custom_alias": "gh"})

    # 2. Check initial stats (0 clicks)
    stats_res = client.get("/api/v1/stats/gh")
    assert stats_res.status_code == 200
    assert stats_res.json()["clicks"] == 0

    # 3. Delete / Deactivate link
    del_res = client.delete("/api/v1/shorten/gh")
    assert del_res.status_code == 200

    # 4. Subsequent redirect attempt must return 404
    redir_res = client.get("/gh", follow_redirects=False)
    assert redir_res.status_code == 404