import logging
import pandas as pd
from datetime import timedelta, datetime
from airflow.decorators import dag, task
import pathlib
from etl.interactions.user_interactions import UserInteractionDataExtract, UserInteractionDataTransform, UserInteractionDataLoad


default_args = {
    'owner': 'Airflow',
    'email_on_failure': True,
    'email': ['your_email@example.com'],
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 6),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

logger = logging.getLogger(__name__)
#######################################################################


@dag(schedule="@daily", default_args=default_args, catchup=False)
def user_interaction_dag():
    @task
    def extract_user_interaction_data():
        """
        Gets the data from csv file
        """
        path = str(pathlib.Path(__file__).parent.parent.resolve().joinpath('DATA/sample.csv'))
        logger.info(f"Extracting the data from csv file given at path {path}.")
        user_extract = UserInteractionDataExtract(path)
        df = user_extract.extract()
        df_json = df.to_json(orient='split', index=False)
        logger.info(f"Loading Complete.")
        return {"raw_data": df_json}

    @task
    def transform_user_interaction_data(raw_data: str):
        """
        Transform raw data
        """

        if raw_data is not None:
            logger.info(f"Reading the data from xcom and transform the data")
            df = pd.read_json(raw_data['raw_data'], orient='split')
            user_transform = UserInteractionDataTransform(df)
            df = user_transform.transform()
            df_json = df.to_json(orient='split', index=False)
            return {"transformed_data": df_json}
        else:
            logger.info(f"Recieved data from xcom is empty")
            return {"transformed_data": None}
    
    @task
    def load_user_interaction_data(transformed_data: str):
        """Load the data to postgres database"""
        if transformed_data is not None:
            logger.info(f"Loading the data to postgres data.")
            df = pd.read_json(transformed_data['transformed_data'], orient='split')
            user_load = UserInteractionDataLoad(df, table_name='interactions')
            user_load.load()



    # Invoke functions to create tasks and define dependencies
    load_user_interaction_data(transform_user_interaction_data(extract_user_interaction_data()))


user_interaction_dag()
