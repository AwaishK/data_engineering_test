import pandas as pd
import pathlib

from etl.interactions.exceptions import FileFormatNotSupported
from utils.database_connection import SetupDB


class UserInteractionDataExtract:
    """This class is responsible to load data from given csv file, validate data types and clean the data."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

        self.schema = {"interaction_id": int, "user_id": int, "product_id": int, "action": str, "timestamp": str}

        if not self.file_path.endswith("csv"):
            raise FileFormatNotSupported()

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path, dtype=self.schema)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(how="any", axis=0)
        return df.reset_index(drop=True)

    def extract(self) -> pd.DataFrame:
        df = self.load_data()
        df = self.clean_data(df)
        return df


class UserInteractionDataTransform:
    """This class holds all the transformations for the data"""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def transform(self) -> pd.DataFrame:
        df = (
            self.df.groupby(by=["user_id", "product_id"])
            .agg(interaction_count=("interaction_id", "count"))
            .reset_index()
        )
        return df


class UserInteractionDataLoad:
    """This class ensures that table exists in database and loads aggregated data to BQ."""

    def __init__(self, df: pd.DataFrame, table_name: str) -> None:
        self.df = df
        self.table_name = table_name
        self.db = SetupDB()

    def ensure_table_exists(self) -> None:
        self.db.query(Queries.create_interactions_table)

    def load(self) -> None:
        self.ensure_table_exists()
        self.db.load_data_from_dataframe(self.df, table_name=self.table_name)


class Queries:
    """Purpose of this class is to hold all the queries for above ETL process"""

    create_interactions_table = """
        CREATE TABLE IF NOT EXISTS public.interactions(
            user_id integer,
            product_id integer,
            interaction_count integer
        );
"""


def run_pipeline_user_interactions():
    path = str(pathlib.Path(__file__).parent.parent.parent.resolve().joinpath("DATA/sample.csv"))
    user_extract = UserInteractionDataExtract(path)
    df = user_extract.extract()
    user_transform = UserInteractionDataTransform(df)
    df = user_transform.transform()
    user_laod = UserInteractionDataLoad(df, table_name="interactions")
    user_laod.load()


if __name__ == "__main__":
    run_pipeline_user_interactions()
