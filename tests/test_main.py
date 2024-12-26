def test_environment_variables():
    import os
    assert os.getenv("GITHUB_TOKEN") is not None, "GITHUB_TOKEN is missing."
