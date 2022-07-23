from typing import Final

__all__ = (
    "SECOND",
    "MINUTE",
    "HOUR",
    "DAY",
)


SECOND: Final = 1
MINUTE: Final = 60 * SECOND
HOUR: Final = MINUTE * 60
DAY: Final = HOUR * 24
