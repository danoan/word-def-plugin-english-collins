def pytest_addoption(parser):
    parser.addoption("--entrypoint", action="store")
    parser.addoption("--secret-key", action="store")
