import pandas as pd
from datetime import timedelta, datetime
from airflow.decorators import dag, task
import pathlib
from etl.interactions.user_interactions import UserInteractionDataExtract, UserInteractionDataTransform, UserInteractionDataLoad


default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 6),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

schedule_interval = "00 09 * * *"

#######################################################################

# dag = DAG(
#     'user_interactions',
#     default_args=default_args,
#     schedule_interval=schedule_interval,
#     catchup=False,
# )

# # Define tasks
# with dag:
#     user_interactions_extraction = PythonOperator(
#         task_id="user_interactions_extraction", 
#         provide_context=True,
#         op_kwargs={'file_path': 'DATA/sample.csv'},
#         python_callable=user_interactions_extraction
#     )


@dag(schedule="@daily", default_args=default_args, catchup=False)
def user_interaction_dag():
    @task
    def extract_user_interaction_data():
        """
        Gets the data from csv file
        """
        path = str(pathlib.Path(__file__).parent.parent.resolve().joinpath('DATA/sample.csv'))
        user_extract = UserInteractionDataExtract(path)
        df = user_extract.extract()
        df_json = df.to_json(orient='split', index=False)
        return {"raw_data": df_json}

    @task
    def transform_user_interaction_data(raw_data: str):
        """
        Transform raw data
        """

        if raw_data is not None:
            df = pd.read_json(raw_data['raw_data'], orient='split')
            user_transform = UserInteractionDataTransform(df)
            df = user_transform.transform()
            df_json = df.to_json(orient='split', index=False)
            return {"transformed_data": df_json}
        else:
            return {"transformed_data": None}
    
    @task
    def load_user_interaction_data(transformed_data: str):
        if transformed_data is not None:
            df = pd.read_json(transformed_data['transformed_data'], orient='split')
            user_load = UserInteractionDataLoad(df, table_name='interactions')
            user_load.load()



    # Invoke functions to create tasks and define dependencies
    load_user_interaction_data(transform_user_interaction_data(extract_user_interaction_data()))


user_interaction_dag()
