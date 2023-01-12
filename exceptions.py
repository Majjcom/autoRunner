
class ParseErrorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RunTimeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
