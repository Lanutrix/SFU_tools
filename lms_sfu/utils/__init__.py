def href_id(href: str) -> str:
    """'/123-456' -> '123-456'"""
    return href.rsplit("/", 1)[-1]
