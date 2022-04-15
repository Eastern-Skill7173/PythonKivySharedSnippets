from typing import Final

__all__ = (
    "SIUnitsPrefixes",
    "SECOND",
    "MINUTE",
    "HOUR",
    "DAY",
)


class SIUnitsPrefixes:
    """
    Table of SI measurement units' prefixes from tera to kilo
    """
    TERA: Final = 10 ** 12
    GIGA: Final = 10 ** 9
    MEGA: Final = 10 ** 6
    KILO: Final = 10 ** 3


SECOND: Final = 1
MINUTE: Final = 60 * SECOND
HOUR: Final = MINUTE * 60
DAY: Final = HOUR * 24
