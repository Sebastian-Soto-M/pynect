import json
from enum import Enum
import logging
from socket import gethostname
from typing import Dict, List, Optional

import pandas as pd
import pyodbc as dbdriver
from pandas import DataFrame
from pydantic import BaseModel
from pyodbc import Connection as dbconnection
from pyodbc import Cursor
from pynect.api.connector.cli import ConnectorOptions
from pynect.api.connector.models import Connector, ConnectorManager
from pynect.utils import map_dataframe_columns, utils


class DBEnum(str, Enum):
    DENODO = 'denodo'


class DB:
    def __init__(self, connection: dbconnection):
        self.__connection = connection

    @property
    def connection(self) -> dbconnection:
        return self.__connection


class DenodoConnectionOptions(BaseModel):
    driver: str
    field_mappings: Dict[str, str]
    boolean_mappings: Dict[str, bool]
    page_size: int = 1000
    password: Optional[str] = None
    query: str
    server_database: str
    server_name: str
    server_port: int
    user: Optional[str] = None

    def __str__(self) -> str:
        return f'Server: {self.server_name}\tDataBase: {self.server_database}'\
            f'\tPort: {self.server_port}'


class DenodoEnvironment(str, Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'


class DenodoDBConnector(Connector):
    """
    Protocols:
    * PSelect
    """

    def __init__(
        self,
        name: str,
        denodo_options: DenodoConnectionOptions,
        options: ConnectorOptions,
        parse,
        filter
    ):
        """Initialize a DenodoDB object

        Args:
            connection (Optional[dbconnection], optional): Connection object.
            [None]
        """
        self.__denodo_opts = denodo_options
        self.__custom_class = None
        self.__parse = parse
        self.__filter = filter
        Connector.__init__(self, name, options)

    @property
    def dnd_opts(self) -> DenodoConnectionOptions:
        return self.__denodo_opts

    @property
    def cursor(self) -> Cursor:
        return self.__cursor

    @property
    def columns(self) -> list[str]:
        return self.__columns

    @property
    def custom_class(self) -> Optional[type]:
        return self.__custom_class

    def __get_class(self, df: DataFrame) -> type:
        def constructor(self, **kwargs):
            for k in kwargs.keys():
                if hasattr(self, k):
                    self.__setattr__(k, kwargs[k])

        def repr(self) -> str:
            return json.dumps(self.__dict__, indent=4)

        df = df.reindex(sorted(df.columns), axis=1)
        attrs = {name: '' for name in df.columns}
        dynamic_class_name = f'{self.name}_class'

        dynamic_class = type(dynamic_class_name, (object, ), {
            "__init__": constructor,
            "__repr__": repr,
            "logger": logging.getLogger(dynamic_class_name),
            "parse": self.__parse,
            "filter": self.__filter,
            **attrs
        })
        self.logger.debug(f'Created a class named "{dynamic_class.__name__}"')
        self.logger.debug(dir(dynamic_class))
        return dynamic_class

    def __execute(self, query: str, **params) -> Cursor:
        self.__cursor = self.__connection.cursor().execute(query, **params)
        self.__columns = [utils.camel_to_snake(
            i[0]) for i in self.cursor.description]
        return self.cursor

    def execute(self):
        client_hostname = gethostname()
        useragent = "%s-%s" % (dbdriver.__name__, client_hostname)
        with dbdriver.connect(
            driver=self.__denodo_opts.driver,
            server=self.__denodo_opts.server_name,
            port=self.__denodo_opts.server_port,
            database=self.__denodo_opts.server_database,
            uid=self.__denodo_opts.user,
            pwd=self.__denodo_opts.password,
            useragent=useragent,
            timeout=600
        ) as connection:
            self.__connection = connection
            self.__execute(self.__denodo_opts.query)
            df = map_dataframe_columns(self.select(
                0), self.__denodo_opts.field_mappings)
            self.__custom_class = self.__get_class(df)
            ConnectorManager(self)()

    def get_objects(self, df: pd.DataFrame) -> list:
        # Parse date columns to string
        df = map_dataframe_columns(df, self.__denodo_opts.field_mappings)
        date_columns = df.select_dtypes(include=['datetime64']).columns
        df[date_columns] = df[date_columns].astype(str)
        ind_cols = df.filter(regex=(".*_ind")).columns
        df[ind_cols] = df[ind_cols].apply(lambda x: x.astype(
            str).str.lower()).replace(self.__denodo_opts.boolean_mappings)
        condition_cols = df.filter(regex=("is_.*")).columns
        df[condition_cols] = df[condition_cols].apply(lambda x: x.astype(
            str).str.lower()).replace(self.__denodo_opts.boolean_mappings)
        records = df.to_dict(orient='records')
        return [self.custom_class(**document)
                for document in records]

    def select_all(self) -> pd.DataFrame:
        """Returns a DataFrame containing all the remaining rows in the query.

        Args:
            df: DataFrame. Pydantic DataFrame with all the remaining records.
        """
        # Output results as pandas dataframe
        return pd.DataFrame.from_records(
            self.cursor.fetchall(), columns=self.columns)

    def select(self, size: int) -> pd.DataFrame:
        """
        Returns a DataFrame containing the remaining rows, containing no more
        than size rows, used to process results in chunks. The list will be
        empty when there are no more rows.

        Args:
            df: DataFrame. Pydantic DataFrame with the remaining records.
            size: int. The number of records to fetch from the DB.
        """
        # Output results as pandas dataframe
        df = pd.DataFrame.from_records(
            self.cursor.fetchmany(size), columns=self.columns)
        self.logger.info(
            'Queried database with a page size of '
            f'{size} and got {len(df.index)} records')
        return df

    def configure(self):
        super().configure()

    def gather_all_data(self) -> List[str]:
        paths = []
        gathered_documents = 0
        try:
            documents: list = []
            size = int(self.opts.max_size)
            while len((data := self.get_data(self.dnd_opts.page_size))) != 0:
                if len(documents) > size:
                    self.logger.info(format(
                        'Data quantity reached the max size of %d',
                        self.opts.max_size
                    ))
                    documents += data
                    gathered_documents += len(data)
                    paths.append(self._persist_data(documents[:size]))
                    del documents[:size]
                else:
                    documents += data
                    gathered_documents += len(data)
            paths.append(self._persist_data(documents))
            self.logger.info(
                f'Final amount of documents gathered: {gathered_documents}')
            self.logger.info(f'Files created: {paths}')
        except KeyError as e:
            self.logger.error(f'There was an error getting data:\n{e}')
        return paths

    def get_data(self, page_size: int) -> Optional[list]:
        df = self.select(page_size)
        documents = self.get_objects(df)
        valid_documents = []
        for doc in documents:
            if doc.filter():
                doc.parse()
                valid_documents.append(doc)
        data = [doc.__dict__ for doc in valid_documents if doc is not None]
        self.logger.info(
            'Documents from page\t=\t'
            f'{len(documents)}\tAfter filtering\t=\t{len(data)}')
        return data
