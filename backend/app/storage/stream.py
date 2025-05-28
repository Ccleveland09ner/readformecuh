class StreamStorage:
    """
    No-op storage used when STORAGE_MODE=stream.
    The caller gets the raw bytes and decides how to send them.
    """
    def save(self, data: bytes, *args, **kwargs) -> bytes:
        return data          