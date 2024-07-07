# QUICK START

## PROJECT STRUCTURE

```bash

├── dags
│   ├── user_interactions.py                  
│   │   │ 
│── DATA
│   │── sample.csv
│   │   │ 
│── data_storage_and_retrieval
│   │── user_interactions_raw.sql  
│   │── user_interactions_retrieval.sql
│   │   │  
├── etl
│   │── interactions
│   │   │── exceptions.py
│   │   │── user_interactions.py
├── utils
│   │── config_parser.py
│   │── database_connection.py
│   │   │
└── README.md
└── Makefile
└── requirements.txt
└── config.ini
└── .env
└── env
└── airflow.cfg
└── .gitignore
```

## Database 

Please ensure you have postgres database with the name `users` 

## Installation & Setup

Run the following commands to clone the project and then create virtual enviroment

```bash
git clone git@github.com:AwaishK/data_engineering_test.git
cd data_engineering_test
make dev-env
```

Please use below given template to create a config file 
config_dot_ini_template is dummy file, please you same configuration but remember to change username and password

```bash
    config_dot_ini_template -> config.ini
```

Please use below given template to create a .env file
dot_env is dummy file, please use same env variables but remember to update the values

```bash
    dot_env -> .env
```

Run the following command to add environemtns variable to your virtual env

```bash
printf "\nexport \$(grep -v '^#' .env | xargs)" >> env/bin/activate
```


### Note: 

I am using the same database for all the tasks. `user_interactions_db.sql` file contains the dump of the data. 

## TASK 1

Please run below command to run the data pipeline

```bash
    python etl/interactions/user_interactions.py
```

## TASK 2  
Make sure to perform Installation and Setup steps. 

Please run the following command to install a standalone airlfow server
& use default username and password shown in console 

```bash
    make setup-airflow
```

### Improvements
Although we are using a standalone server here for the purpose of this task. 
But we can improve it to use production version of airflow by using its official docker images. 
Also using persistent volumes to store the airflow metadata and logs. 

Also we could also use postgres connection directly from airflow instead of implementing it ourself using python. But I am trying to reuse what 
I have built for the Task1. 

```bash
pip install apache-airflow-providers-postgres
```

## TASK 3

We have a folder called `data_storage_and_retrieval` where we have two files named `user_interactions_raw.sql` & `user_interactions_retrieval.sql`.

1. `user_interactions_raw.sql`
    Above file contains the queries to create the table schema in postgres database. 
    and load the data from csv file to postgres itself. 

2. `user_interactions_retrieval.sql`
    Above file contains retrieval queries to answer the questions asked in TASK-3.

### Optimizations 
I have used interaction_id, user_id, product_id combinations as primary key. 
    1. It provides a unique combinations for a user and production, a single interaction must be a unique identifier. 
    2. These three are mainly being used in group by clause and having them a primary key automatically add a multi column index will make the queries faster. 
I added the index on timestamp as well. because it is possible that we will be queries the table to get data based on datetime for analysis purposes. 

To keep up wtih the performance during inserts, we might need to drop index and re-add afterwards. 
