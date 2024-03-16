from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def keys(cls) -> list[str]:
        return [elem.name for elem in cls]

    @classmethod
    def values(cls) -> list[str | int]:
        return [elem.value for elem in cls]


class BaseStrEnum(str, BaseEnum):
    @classmethod
    def get(cls, name: str) -> str:
        try:
            return getattr(cls, name).value
        except AttributeError:
            raise AttributeError(f'Attribute {name} not found.')


class Action(BaseStrEnum):
    echo: str = 'echo'
