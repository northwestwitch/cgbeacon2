
from cgbeacon2.constants import MISSING_PUBLIC_KEY
from cgbeacon2.utils.auth import elixir_key

def test_elixir_key_wrong_key():
    """Test function that returns Elixir AAI public key with wrong server"""

    public_key = elixir_key("nonsense")
    assert public_key==MISSING_PUBLIC_KEY

def test_elixir_key(mock_app):
    """Test the function that returns the public key of Elixir AAI"""

    # When calling the Elixir OAuth2 server
    oauth_config = mock_app.config.get("ELIXIR_OAUTH2")
    assert "server" in oauth_config

    # It should return the expected keys
    public_key = elixir_key(oauth_config["server"])
    assert public_key["keys"][0]["alg"] # algorithm
    assert public_key["keys"][0]["kid"]
    assert public_key["keys"][0]["n"]
    assert public_key["keys"][0]["kty"]
