
from typing import List, Union, NewType

Snowflake = NewType('Snowflake', int)

RawSnowflake = Union[str, int]
SnowflakeList = List[Snowflake]