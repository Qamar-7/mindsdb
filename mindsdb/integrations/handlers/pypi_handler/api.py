from os import path
from typing import Collection, Dict

import numpy as np
import pandas as pd
import requests

BASE_URL = r"https://pypistats.org/api/packages/"


class PyPI:
    def __init__(self, name: str) -> None:
        """initializer method

        Args:
            name(str): package name
        """
        self.name: str = name
        self.endpoint: str = path.join(BASE_URL, name)
        print(self.endpoint)

    def recent(self, period: str = None) -> pd.DataFrame:
        """recent endpoint

        Args:
            period (str, optional): the desired `day` or `week` or `month` period. Defaults to None.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        endpoint: str = path.join(self.endpoint, "recent")
        params: Dict = {}

        if period:
            params["period"] = period

        payload = requests.get(endpoint, params=params).json()["data"]

        df = self.__to_dataframe(payload, [0])

        return df

    def overall(self, mirrors: bool = None) -> pd.DataFrame:
        """overall endpoint

        Args:
            mirrors (bool, optional): filter by mirrors. Defaults to None.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        endpoint: str = path.join(self.endpoint, "overall")
        params: Dict = {}

        if mirrors is not None:
            params["mirrors"] = str(mirrors).lower()

        payload = requests.get(endpoint, params=params).json()["data"]
        df = self.__to_dataframe(payload)

        return df

    def python_major(
        self, version: str = None, include_null: bool = True
    ) -> pd.DataFrame:
        """python major endpoint

        Args:
            version (str, optional): filter by the major version number. Defaults to None.
            include_null (bool, optional): include the null records as well. Defaults to True.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        endpoint: str = path.join(self.endpoint, "python_major")
        params: Dict = {}

        if version is not None:
            params["version"] = version

        payload = requests.get(endpoint, params=params).json()["data"]
        df = self.__to_dataframe(payload, include_null=include_null)

        return df

    def python_minor(
        self, version: str = None, include_null: bool = True
    ) -> pd.DataFrame:
        """python minor endpoint

        Args:
            version (str, optional): filter by the minor.patch version number. Defaults to None.
            include_null (bool, optional): include the null records as well. Defaults to True.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        endpoint: str = path.join(self.endpoint, "python_minor")
        params: Dict = {}

        if version is not None:
            params["version"] = version

        payload = requests.get(endpoint, params=params).json()["data"]
        df = self.__to_dataframe(payload, include_null=include_null)

        return df

    def system(self, os: str = None, include_null: bool = True) -> pd.DataFrame:
        """system endpoint

        Args:
            os (str, optional): filter by the operating system. Defaults to None.
            include_null (bool, optional): include the null records as well. Defaults to True.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        endpoint: str = path.join(self.endpoint, "system")
        params: Dict = {}

        if os is not None:
            params["os"] = os

        payload = requests.get(endpoint, params=params).json()["data"]
        df = self.__to_dataframe(payload, include_null=include_null)

        return df

    @staticmethod
    def __to_dataframe(
        json_data: Dict, index: Collection = None, include_null: bool = True
    ) -> pd.DataFrame:
        """converts the raw json to pandas dataframe

        Args:
            json_data (Dict): data
            index (Collection, optional): desired index. Defaults to None.
            include_null (bool, optional): dropping or keeping the null records. Defaults to True.

        Returns:
            pd.DataFrame: pandas dataframe
        """
        df = pd.DataFrame(json_data, index=index)
        df.replace("null", np.nan, inplace=True)

        if include_null is False:
            return df.dropna()
        return df
