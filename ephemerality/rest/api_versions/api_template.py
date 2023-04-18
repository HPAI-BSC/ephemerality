from abc import ABC, abstractmethod
from typing import Annotated, Sequence
from fastapi import Query
from ephemerality import ResultSet


class AbstractRestApi(ABC):
    @staticmethod
    @abstractmethod
    def version() -> str | None:
        return None

    @abstractmethod
    def get_ephemerality(self,
                         input_vector: Sequence[float],
                         threshold: Annotated[float, Query(gt=0., le=1.)],
                         types: Annotated[str, Query(Query(min_length=1, max_length=4, regex="^[lmrs]+$"))]
                         ) -> ResultSet:
        raise NotImplementedError
