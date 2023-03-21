from __future__ import annotations
from time import sleep

from typing import Optional


class RestAPIQuery:
    def __init__(
            self, base_url: str, prefix: str = '', suffix: str = '',
    ) -> None:
        self.base_url = base_url
        self.prefix = prefix
        self.suffix = suffix

    @property
    def endpoint(self):
        return self.base_url

    def __call__(self, path_params: Optional[str] = None, **kwargs) -> Any:
        if kwargs:
            return (f'{self.endpoint}/{path_params}?'
                    if path_params else f'{self.endpoint}?') + '&'.join([
                        f'{self.prefix}{k}={v}{self.suffix}'
                        for k, v in kwargs.items()
                    ])
        else:
            return self.endpoint
