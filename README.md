<h1 align=center><strong>Fastapi Microservice Template</strong></h1>

A template to jumpstart your microservice projects using FastAPI. This repository provides a structured foundation inspired by real-world applications, so you can focus on building features instead of boilerplate.
> ⚠️ This template is not a drop-in production deployment, but it’s built on production-grade principles (modular architecture, service discovery, API gateway, centralized config). It gives you a strong foundation to scale toward production.

<img width="1922" height="1004" alt="fastapi-microservice" src="https://github.com/user-attachments/assets/fd62300a-cd62-4b5c-bc9c-7f56c0a5cc74" />

## What's The Tech-Stack?
* 🐳 [Dockerized](https://www.docker.com/)
* 🐘 [Asynchronous PostgreSQL](https://www.postgresql.org/docs/current/libpq-async.html)
* 🐍 [FastAPI Backend Boilerplate](https://fastapi.tiangolo.com/)
* 💾 [Alembic Auto Migration](https://github.com/sqlalchemy/alembic)
* ☎️ [Consul Service Registry](https://www.hashicorp.com/en/products/consul)
* 📑 [Consul KV](https://www.hashicorp.com/en/products/consul)
* 👮 [Kong Gateway](https://konghq.com/products/kong-gateway)
* 🪪 [Registrator](https://hub.docker.com/r/hypolas/registrator)
* 🗂️ [UV package manager](https://docs.astral.sh/uv/)

## What's The Boilerplate Structure?
```shell
.github/
├── workflows/
    ├── docker-publish.yml              # A CI file for the backend app that connected to github container registry
service-a/
├── app/
    ├── api/
        ├── dependencies/               # Dependency injections folder
        ├── routes/                     # Endpoints
            ├── service_routes.py       # Service's routes / controller
        ├── endpoints.py                # Endpoint registration
    ├── config/
        ├── settings/
            ├── base.py                 # Base settings / settings parent class
                ├── development.py      # dev env settings
                ├── environments.py     # Enum with PROD, DEV, STAGE environment
                ├── production.py       # prod env settings
                ├── staging.py          # uat env settings
        ├── events.py                   # Registration of global events
        ├── manager.py                  # Manage config properties fetch to consul kv or local .env
    ├── model/
        ├── db/
            ├── account.py               # Pokemon class for database entity
        ├── schemas/
            ├── global_response.py       # Standardized global api response wrapper to promote consitency
            ├── pokemon_dto.py           # Pokemon Data Transfer Object classes for data encapsulation and validation
            ├── base.py                  # Base class with pydantic for data validation objects
    ├── repository/
        ├── crud/
            ├── pokemon_repository.py   # Repository class for C. R. U. D. operations for Pokemon entity
            ├── base.py                 # Base class for C. R. U. D. operations
        ├── migrations/
            ├── versions/               # Generated migration scripts for tracking database schema changes history,
            ├── env.py                  # Generated via alembic for automigration (adjusted for specific schema)
            ├── script.py.mako          # Generated via alembic
        ├── proxy/
            ├── service_b_proxy.py      # Proxy class (client) to call other remote services via consul service discovery
            ├── base.py                 # Base class for proxy / client communication
        ├── base.py                     # Entry point for alembic automigration
        ├── database.py                 # Database class with engine and session
        ├── events.py                   # Registration of database events
        ├── table.py                    # Custom SQLAlchemy Base class
    ├── api/
        ├── crud_service.py             # Service layer for storing all business logic
    ├── utilities/                      # Folders to store your util class and logic
        ├── datetime_formatter.py
├── .env-example                        # Our bootstrap properties in local development (rename this to '.env') 
├── .env-local                          # Our application properties based on environtment (fell free to add .env-staging, prod, etc) 
├── Dockerfile                          # Docker configuration file for backend service
├── README.md                           # Documentation for backend app
├── alembic.ini                         # Automatic database migration configuration (adjusted for specific schema)
├── main.py                             # Our main backend server app
├── pyproject.toml                      # Our source of truth for project metadata, dependencies, and build system
├── requirements.txt                    # Packages installed and list of dependency for backend app
├── uv.lock                             # lockfile generated by uv
```

## What's The Scenario?
we'll have two primary interaction flows, orchestrated through an API Gateway.

### 1st Scenario : Find a Trainer for a Pokémon
``` shell
Client -> GET {gateway_url}/pokemons/get-data -> Service-A -> Service-B -> Client
```
Workflow:
1. A client sends a GET request to `/pokemons/get-data` endpoint on the API Gateway.
2. The gateway routes the request to `service-a` (the Pokémon Service).
3. `service-a` fetches data for a random Pokémon.
4. `service-a` then calls `service-b` (the Trainer Service) to find a trainer who would be a good match for the selected Pokémon.
5. The combined Pokémon and Trainer data is aggregated and returned to the client. The response will look like below example

<p align="center">
  <img src="https://github.com/user-attachments/assets/7840747a-933e-4ea2-bfa3-3645bd7633dd" alt="1st journey pokemon to trainer" width="400"/>
</p>

### 2nd Scenario: Find a Pokémon for a Trainer
``` shell
Client -> GET {gateway_url}/trainers/get-data -> Service-B -> Service-A -> Client
```
Workflow:
1. A client sends a GET request to `/trainers/get-data` endpoint on the API Gateway.
2. The gateway routes the request to `service-b` (the Trainer Service).
3. `service-b` fetches data for a random trainer.
4. `service-b` then calls `service-a` (the Pokémon Service) to find a Pokémon that fits the trainer's profile or specialty.
5. The combined Trainer and Pokémon data is aggregated and returned to the client. The response will look like below example

<p align="center">
  <img src="https://github.com/user-attachments/assets/9ea6c7bf-ed16-4cd3-becd-87084908f007" alt="2nd journey trainer to pokemon" width="400"/>
</p>


## How to Setup?
This project is now structured using multiple docker-compose files to separate the core infrastructure from the application services. This is the practice for managing different service lifecycles and environments.
```shell
├── docker-compose.yml           # Application services (service_a, service_b, etc.)
├── docker-compose.infra.yml     # Infrastructure (PostgreSQL, Consul, Registrator, Kong)
└── postgres-init/
    └── init-multi-db.sh         # bootstrap file for Postgres
```

### 1. Start the Infrastructure Stack
First, launch the infrastructure services like the database, service discovery, and API gateway.
```shell
docker-compose -f docker-compose.infra.yml up -d
```
After that check all containers, ensure their healthiness.
> ℹ️ Note: The `kong-bootstrap` container is expected to run once to set up the database and then exit. Seeing it with a status of `Exited (0)` is normal.

### 2. Verify Database Initialization
The `postgres-init` script automatically creates the necessary databases and schemas. Connect to your PostgreSQL instance and verify that the following structure exists:
```plaintext
├── kong
    └── public
        └── 35 Kong's internal tables)
├── microservice
    └──service_a
    └──service_b
```

### 3. Setup & Inspect Consul Service Registry
Consul provides a UI to inspect the service mesh and manage configuration.
> using UI is not weak, it not just easier, but help us reduce human error 😎

1. Verify Service Registration:
Open the Consul UI at `http://localhost:8500` Navigate to the Services tab. You should see `service-a` and `service-b` listed as healthy.
<p align="center">
<img src="https://github.com/user-attachments/assets/fbb27c7c-1ce9-4531-b7a6-3047721341b2" alt="Consul Services UI" width="700"/>
</p>
2. Set Up Centralized Configuration:
Use the Key/Value tab to store centralized configuration that your services will use, get the config in `.env-local`.
<p align="center">
<img src="https://github.com/user-attachments/assets/1108ce91-7836-49e1-8a03-860b8f75cae0" alt="Consul Key/Value UI" width="700"/>
</p>

### 3. Start the Application Services
```shell
docker-compose -f docker-compose.yml up -d
```
when every time service is starting... it will try to migrate the migrations using `alembic`. So table that we devine in code base will also created in the database.
before you can fully use the app endpoint, insert application's data in `postgres-init\example-data.sql`
> (ℹ️) DO NOT change version data in `*/app/repository/migration/versions/*.py`, if you need to change the migration follow instruction at section 'How To Modify The Code?'



### 5. Finale; Setup Your Gateway
same like consul, our Kong gateway also provide intuitive web admin UI 
first create your services, add service-a to kong i setup like below
```json
{
  "name": "pokemon-service",
  "tags": null,
  "protocol": "http",
  "host": "service-a.service.consul",
  "path": "/service-a/",
  "port": 80
}
```
do the same to service-b
```json
{
  "name": "trainer-service",
  "tags": null,
  "protocol": "http",
  "host": "service-b.service.consul",
  "path": "/service-b/",
  "port": 80
}
```

after above configuration you'll get something like below:
![WhatsApp Image 2025-09-06 at 23 54 27_7a1b7cf9](https://github.com/user-attachments/assets/32c5cd0c-b118-4404-a9e0-4a120a48389d)


Next setup your route, i make every request with `/pokemons` is redirected to `service-a` aka `pokemon-service`
```json
{
  "name": "pokemon-service-route",
  "service": {
    "id": "13202838-f1b8-43f0-b541-8a15acaac2d5"
  },
  "tags": [],
  "protocols": [
    "http"
  ],
  "paths": [
    "/pokemons"
  ]
}
```

do the same to service be every request with `/trainers` is redirected to `service-b` aka `trainer-service`
```json
{
  "name": "trainer-service-route",
  "service": {
    "id": "69b874d5-0b86-4292-8b81-563d64df37a4"
  },
  "tags": [],
  "protocols": [
    "http"
  ],
  "paths": [
    "/trainers"
  ]
}
```

after above configuration you'll get something like below:
![WhatsApp Image 2025-09-06 at 23 54 26_ee4e3ff5](https://github.com/user-attachments/assets/e8758bf3-5218-4713-9e15-93c9d8ae0612)


## How To Modify The Code?
0. ensure you have uv package manager installed
1. go to root project `python-fastapi-microservice/service-a/`, activate venv, sync and install all required dependency form uv.lock `uv sync`, we are using uv in this project, but keep the requirements.txt on track by exporting it

2. `alembic revision --autogenerate -m "Create pokemons table"` will generate app/repository/migration/versions/xxxx_xxxx_table.py. so use it when you modify or create new table. after versions file is generated, then just start the service again, the automigration will start migrating your changes

3.  run the service `python main.py`

