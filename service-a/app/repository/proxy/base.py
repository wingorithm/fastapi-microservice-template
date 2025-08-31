import httpx

class BaseProxy:
    """
    @BaseProxy -> act like Constructor for all proxy / client implementations
    """
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)