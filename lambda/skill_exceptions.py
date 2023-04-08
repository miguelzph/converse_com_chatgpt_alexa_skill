class FullUsageLimitError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class RequestOpenAPIError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)