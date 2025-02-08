class ImageRetrievalException(Exception):

    def __init__(self, message: str, e: Exception):
        self.message = message
        super().__init__(e)

    def __str__(self):
        return f"{self.message}"
