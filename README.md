# Oryx War Losses - The Daily Tracking of Infantry Vehicle Losses In The Russo-Ukrainian War

A small ETL pipeline that pulls data from the web to feed an interactive dashboard.

## Table of Contents

- [Introduction](#introduction)
- [Interactive Dashboard View](#interactive-dashboard-view)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)

## Introduction

This project is an ETL pipeline that automatically scrapes and stores on a daily basis a summary of infantry vehicle related losses resulting from the armed conflict between the Russian Federation and Ukraine, started on the 24th of February, 2022. The data is taken from the Oryx website - a platform dedicated to collecting evidence and validating this type of occurrences, and pipelined to an interactive dashboard implementation that allows to visually observe and compare the evolution of such losses:
- Compare between types of losses: destroyed, damaged, abandoned, captured.
- Compare between types of vehicle lost: tanks, armoured fighting vehicles, etc.
- Compare ukrainian and russian losses vis-a-vis.

### Interactive Dashboard View

![img_1](img/screenshot_1.png)

![img_2](img/screenshot_2.png)

![img_3](img/screenshot_3.png)

## Features

- Scraping process and database pipelining via Scrapy framework.
- Scraped data and environment variables validation with Pydantic. 
- MySQL database for data storage.
- SQLAlchemy for database setup and connection.
- Alembic for data model migration.
- Airflow for task orchestration.
- X Array for data processing.
- Plotly for data visualization.
- Dash for front-end dashboard implementation.
- Pytest for multiple purpose testing.   

##### Additional features:
- Implementation of a small mechanism that tells Airflow to mark a DAG run as a 'failure' if the Scrapy log catches non-critical errors before and after the current crawling/scraping/pipelining process. 

- Implementation of an auto-flusher for the Scrapy log file after 10 spider combined runs (two spiders, one that scrapes Ukraine related data end other that scrapes Russia related data, are run sequentially via the same `spider_runner` script, therefore, two logs are appended to the log file each cycle).      

##### Notes:
- This projects uses an airflow version for development - ['airflow standalone'](https://airflow.apache.org/docs/apache-airflow/stable/start.html), which uses a simpler implementation when compared to the production setup.


## Getting Started 

(For Linux machines)

Integrating Airflow into a project requires additional septs and considerations:

- [Poetry](https://python-poetry.org/) ins't compatible; regardless it is highly recommended to use a virtual environment with a dependency manager that automatically finds/'locks' package compatibility.

- The deployment of Airflow is usually made via a container/Docker framework; for development purposes, we can make it work via Python `venv`/`pipenv`. When activating a virtual environment via [Pipenv](https://pipenv.pypa.io/en/latest/index.html) environment variables are loaded in advance, enabling the Airflow root directory to be [recognized](https://stackoverflow.com/questions/56890937/how-to-use-apache-airflow-in-a-virtual-environment).   


### Installation

This installation process assumes that [MySQL](https://dev.mysql.com/doc/refman/8.0/en/postinstallation.html) has been installed locally. 

Pipenv can throw errors when working with a Python version different from the one used to create the virtual environment and the lock file; in this case we can use Pyenv to install the specific Python version used in this project: Python 3.8. 

Install Pyenv following [these instructions](https://github.com/pyenv/pyenv), then:

Fetch a specific version to be installed:

        $ pipenv --python 3.8.15 install 

Install Pipenv:

        $ pip3 install --user pipenv

Create the projets's virtual evironment with the same Python version fetched by Pyenv:

        $ cd path/to/project/root/folder
        $ pipenv shell
        $ pipenv install --python 3.8.15

Verify if the specified Python version was successfully installed (the virtual environment must be active):

        $ python --version

Install the required packages.

        $ pipenv install -r requirements/requirements.txt

Create database tables in the MySQL database with Alembic (it is assumed that the database schema has already been set on the server side):

        $ alembic upgrade head

#### Airflow setup:

Set two environment variables: `AIRFLOW_HOME` sets the `airflow` folder in the project's root folder path; adding both, project's root and airflow paths, to `PYTHONPATH`, allows the DAG script
to import modules outside de scope set in `airflow.cfg`.  

        $ echo "AIRFLOW_HOME=${PWD}/airflow" > .env
        $ echo "PYTHONPATH=${PWD}:${PWD}/airflow" >> .env


At this stage the `airflow` folder only contains the `dags` folder with the DAG script necessary for this project; the next command sets the Airflow components, initializes the database, creates an admin, and starts all components. 
        
        $ airflow standalone

#### Notes: 

- To activate the DAG, access the UI via admin with the password generated by the last command `standalone_admin_password.txt`; search for the project's DAG via tag - 'oryx', or name - 'scrapy_pipeline', and unpause it.  

- For Airflow to recognize the DAGs script inside the `dags` folder after relocation, it may be required to shut Airflow down and re-run `airflow standalone`. To avoid loading DAG examples provided by Airflow set `load_examples` to `False` inside `airflow.cfg`.

- To set a specific time for the DAG to run change the `schedule` parameter in `./airflow/dags/dag_scrapy_pipeline.py` (currently set to run daily at 2 p.m).


### Configuration

#### Environment variables

The project has two .env files: 

- As previously seen on the Airflow setup, one is located in the root folder:

        AIRFLOW_HOME=/path/to/airflow/root/folder

- The other .env file stores all other variables and is located outside the project's directory. It is load via the `env_model.py` script and its path can be assigned to the `dotenv_path` variable. The variables are:

        # MySQL server / database credentials.
        USER_NAME=
        SECRET_KEY=
        PORT=
        HOST=
        DATABASE=


## Usage

There are three 'runner' scripts:

Handled by Airflow:

- `spider_runner`: runs the spiders' jobs 
- `log_check_runner.py`: checks if previous runs had any errors during the execution.

Initiating the dashboard:

        $ python3 dashboard_runner.py 


## License

MIT License