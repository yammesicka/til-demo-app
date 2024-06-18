class TilError(Exception):
    pass


class TilConfigNotFoundError(TilError):
    pass


class TilAiCantExpandIdeaError(TilError):
    pass
