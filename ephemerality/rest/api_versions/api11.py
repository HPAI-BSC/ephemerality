from typing import Sequence, Annotated

from fastapi import Query

from ephemerality.rest.api_versions.api_template import AbstractRestApi
from ephemerality.src import compute_ephemerality, ResultSet


class RestAPI11(AbstractRestApi):
    @staticmethod
    def version() -> str:
        return "1.1"

    @staticmethod
    def get_ephemerality(
            input_vector: Sequence[float],
            threshold: Annotated[float, Query(gt=0., le=1.)],
            types: Annotated[str, Query(Query(min_length=1, max_length=4, regex="^[lmrs]+$"))]
    ) -> ResultSet:
        return compute_ephemerality(activity_vector=input_vector, threshold=threshold, types=types)
