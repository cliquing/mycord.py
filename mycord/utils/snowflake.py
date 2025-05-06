
from typing import List, Union

#Snowflake = NewType('Snowflake', int)

Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]