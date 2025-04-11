# Spotify ETL Pipeline with Apache Airflow, PostgreSQL & Python

This project implements an ETL pipeline to extract recently played tracks from the Spotify API, transform the data, and load it into a PostgreSQL database — all orchestrated with Apache Airflow and Docker.

---
## Tech Stack used

- **Apache Airflow** for orchestration
- **PostgreSQL** for data storage
- **Docker** for containerization
- **Spotify API** for data source
- **Python**

## Features

- Automated ETL using Airflow DAG
- Extract data from Spotify's `recently-played` endpoint
- Data quality checks & transformation (top artists)
- Store raw and transformed data in PostgreSQL
- Containerized with Docker for ease of setup

## 🗂️ Project Structure
```.
├── dags/
│   └── spotify_final_dag.py
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── spotify_etl.py
│   └── auth.py
├── auth_server.py
└── docker-compose.yaml
```

## Prepare Spotify Credentials 
1. Register an app at the Spotify Developer Dashboard https://developer.spotify.com/dashboard/, then generate:
- client_id
- client_secret

2. Save the credentials in .env file:
```
SPOTIFY_CLIENT_ID=*****
SPOTIFY_CLIENT_SECRET=*****
```
3. Run the auth_server.py script. This will use the client credentials and authorize the user and get the refresh_token and save it in a token_info.json file. (This is a one time process)

## Starting Services
Run Docker from the root directory.
```
docker-compose up --build
```
Now the Airflow should be accessible at http://localhost:8080/ 
Add the client id and secret in Connections.
- Go to Admin → Connections
- Click “+” (Add a new connection)
Fill in the details:
- Conn Id: spotify_api
- Conn Type: Generic
- Store client_id, client_secret as a dictionary

  
Add the token_info.json details as Variable in Airflow.
- Go to Airflow UI → Admin → Variables
- Add a new variable:
- Key: spotify_token_info
- Value: Copy the contents of JSON file






