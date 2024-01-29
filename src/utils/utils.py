def ts_now(in_ms: bool = False) -> int:
    import time
    unix_timestamp = time.time()
    if in_ms:
        unix_timestamp *= 1000
    return int(unix_timestamp)