class CodeBlock:
    def __init__(self, lang_type: str, code: str):
        self.lang_type = lang_type
        self.code = code

    @property
    def code_bytes(self) -> bytes:
        return self.code.encode("utf-8")
