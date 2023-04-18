import numpy as np
from pydantic import BaseModel


class ResultSet(BaseModel):
    """Class to contain ephemerality and core size values by subtypes"""
    len_left_core: int | None = None
    len_middle_core: int | None = None
    len_right_core: int | None = None
    len_sorted_core: int | None = None

    eph_left_core: float | None = None
    eph_middle_core: float | None = None
    eph_right_core: float | None = None
    eph_sorted_core: float | None = None

    def __eq__(self, other) -> bool:
        if isinstance(other, ResultSet):
            if \
                    self.len_left_core != other.len_left_core or \
                    self.len_middle_core != other.len_middle_core or \
                    self.len_right_core != other.len_right_core or \
                    self.len_sorted_core != other.len_sorted_core or \
                    not np.isclose(self.eph_left_core, other.eph_left_core) or \
                    not np.isclose(self.eph_middle_core, other.eph_middle_core) or \
                    not np.isclose(self.eph_right_core, other.eph_right_core) or \
                    not np.isclose(self.eph_sorted_core, other.eph_sorted_core):
                return False
            else:
                return True
        else:
            return False
