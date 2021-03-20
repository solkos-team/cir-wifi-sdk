from sdk import set_access_token


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    # set_access_token('user@kof.com', '123abc')

