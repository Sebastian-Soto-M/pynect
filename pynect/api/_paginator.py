from typing import Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor


class ApiPaginator:
    # testing somethign
    def __init__(self,
                 total_pages: int,
                 page_param_name: str,
                 query_builder: Callable[..., str],
                 index: int = 1,
                 path_params: Optional[str] = None,
                 **kwargs
                 ) -> None:
        self.__total_pages = total_pages
        self.__page_param_name = page_param_name
        self.__query = query_builder
        self.__index = index
        self.__path_params = path_params
        self.__kwargs = kwargs

    def build_query(self, index: int) -> str:
        if self.__index == self.__total_pages:
            raise StopIteration
        query = self.__query(
            path_params=self.__path_params,
            **{self.__page_param_name: index},
            **self.__kwargs,
        )
        return query

    def __call__(self) -> Any:
        pool = ThreadPoolExecutor(self.__total_pages)
        results = [pool.submit(self.build_query, i)
                   for i in range(0, self.__total_pages)]
        pool.shutdown()
        return [task.result() for task in results if task.done()]
