from ephemerality.data_processing import InputData
from rest.api import set_test_mode, router
import rest.api_versions as api_versions
from rest.api_versions import AbstractRestApi

__all__ = [
    InputData,
    set_test_mode,
    router,
    AbstractRestApi
]


API_VERSION_DICT: dict[str, AbstractRestApi] = {api.version(): api for api in api_versions.__all__ if api.version()}
DEFAULT_API: AbstractRestApi = API_VERSION_DICT[max(API_VERSION_DICT.keys())]
