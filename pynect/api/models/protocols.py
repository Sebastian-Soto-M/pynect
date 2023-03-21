from typing import Optional, Protocol, Any
from requests import Response


class PUpdate(Protocol):
    """Protocol for objects that can update data"""

    def update(
        self,
        data: dict,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
        **kwargs
    ) -> Response:
        """Performs Api Update

        Args:
            data (dict): Data to update
            endpoint (Optional[str], optional): Api endpoint path. [None]
            params (Optional[dict], optional): all keywords and values for the
            query. [None]

        Returns:
            Response: Result from the Api call.
        """
    ...


class PSelect(Protocol):
    """Protocol for objects that can select data (query)"""

    def select(
        self,
        endpoint: Optional[str] = None,
        params: Optional[dict] = None,
        **kwargs
    ) -> Response:
        """Queries Api with the params provided

        Args:
            endpoint (Optional[str], optional): Api endpoint path. [None]
            params (Optional[dict], optional): all keywords and values for the
            query. [None]

        Returns:
            Response: Result from the Api call.
        """
    ...


class PDelete(Protocol):
    """Protocol for objects that can delete data"""

    def delete(self, endpoint: str, **kwargs) -> Response:
        """Performs Api Delete

        Args:
            endpoint (str): Api endpoint path

        Returns:
            Response: Result from the Api call.
        """
    ...


class PFactory(Protocol):
    """Protocol for objects with get factory method"""
    def get(*args, **kwargs) -> Any: ...
