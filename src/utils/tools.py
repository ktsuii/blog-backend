import re


def extract_ip(address) -> str:
    pattern = re.compile(r'((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)')
    m = pattern.search(address)
    return m.group(0) if m else address
