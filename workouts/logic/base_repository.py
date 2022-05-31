from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from workouts.models.generic.entity import Entity, EntityCreate, EntityUpdate

_T = TypeVar("_T", bound=Entity)
_TCreate = TypeVar("_TCreate", bound=EntityCreate)
_TUpdate = TypeVar("_TUpdate", bound=EntityUpdate)


class Repository(Generic[_T], metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_by_id(id: UUID) -> _T:
        pass

    @staticmethod
    @abstractmethod
    def create(t: _TCreate) -> _T:
        pass

    @staticmethod
    @abstractmethod
    def delete(t: _T) -> None:
        pass

    @staticmethod
    @abstractmethod
    def update(t: _TUpdate) -> _T:
        pass
