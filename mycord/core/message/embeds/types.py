
from typing import List, Literal, TypedDict
from typing_extensions import NotRequired, Required


class EmbedFooter(TypedDict):
    text: str
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]


class EmbedField(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedMedia(TypedDict, total=False):
    url: Required[str]
    proxy_url: str
    height: int
    width: int
    flags: int


class EmbedProvider(TypedDict, total=False):
    name: str
    url: str


class EmbedAuthor(TypedDict, total=False):
    name: Required[str]
    url: str
    icon_url: str
    proxy_icon_url: str


EmbedType = Literal['rich', 'image', 'video', 'gifv', 'article', 'link', 'poll_result']


class EmbedPayload(TypedDict, total=False):
    title: str
    type: EmbedType
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooter
    image: EmbedMedia
    thumbnail: EmbedMedia
    video: EmbedMedia
    provider: EmbedProvider
    author: EmbedAuthor
    fields: List[EmbedField]
    flags: int

