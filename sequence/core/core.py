from abc import ABC, abstractmethod
from itertools import islice
from typing import Generator, List, Any

from sequence.core.utils.validations import validate_positive_integer, validate_as_list_input
from sequence.core.utils.errors import InfiniteSequenceError


class Sequence(ABC):

    @abstractmethod
    def __contains__(self, item):
        raise NotImplementedError

    def __iter__(self):
        return self.as_generator()

    def __getitem__(self, item):
        return self._at(index=item)

    @abstractmethod
    def is_finite(self) -> bool:
        raise NotImplementedError

    @property
    def is_periodic(self) -> bool:
        return False

    @property
    def period(self) -> int:
        return 0

    @abstractmethod
    def as_generator(self) -> Generator:
        raise NotImplementedError

    @abstractmethod
    def as_list(self, end: int, start: int = 0, step: int = 1) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def _at(self, index: int) -> Any:
        raise NotImplementedError


class FiniteType(Sequence, ABC):

    def __init__(self):
        super().__init__()
        self.sequence: List[Any] = None

    def __contains__(self, item: int) -> bool:
        return item in self.sequence

    def as_generator(self) -> Generator:
        for element in self.sequence:
            yield element


class InfiniteType(Sequence, ABC):

    @property
    def is_finite(self) -> bool:
        return False

    def __len__(self) -> int:
        raise InfiniteSequenceError

    def as_list(self, stop: int, start: int = 0, step: int = 1) -> List[int]:
        validate_as_list_input(start=start, stop=stop, step=step)
        return list(islice(self, __start=start, __stop=stop, __step=step))

    def _at(self, index: int) -> int:
        validate_positive_integer(integer=index)
        return next(islice(self, index, index + 1))

