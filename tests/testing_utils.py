class MockedResponse:
    def __init__(self, status_code: int, message: dict):
        self.status_code = status_code
        self.headers = ""
        self.message = message

    def json(self):
        return self.message
