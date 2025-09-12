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
Use the Key/Value tab to store centralized configuration that your serv will use, get the config in `.env-local`.
<p align="center">
<img src="https://github.com/user-attachments/assets/1108ce91-7836-49e1-8a03-860b8f75cae0" alt="Consul Key/Value UI" width="700"/>
</p>

### 4. Start the Application Services
With the infrastructure running, start the service-a and service-b applications.
```shell
docker-compose -f docker-compose.yml up -d
```

On startup, each service automatically runs its database migrations using `Alembic`, creating the tables defined in the codebase.

> ⚠️ Important: To populate the database with sample data required for the endpoints to work, manually execute the SQL commands in `postgres-init/example-data.sql`

> ℹ️ DO NOT change version data in `*/app/repository/migration/versions/*.py`, if you need to change the migration follow instruction at section 'How To Modify The Code?'

### 5. Finale; Setup Your Gateway (Kong)
Finally, expose the services to the outside world by configuring routes in Kong. You can use the Kong Admin UI, available at `http://localhost:8001`.
1. Create an upstream service for `service-a`:
   A Kong Service points to a specific backend. Configure it to use Consul for service discovery.
    - Name: `pokemon-service`
    - Protocol: `http`
    - Host: `service-a.service.consul` (This special address lets Kong find `service-a` via Consul)
    - Port: `80`
2. Create an upstream service for `service-b`:
   Do the same for the trainer service.
    - Name: `trainer-service`
    - Protocol: `http`
    - Host: `service-b.service.consul`
    - Port: `80`
    <p align="center"><img src="https://github.com/user-attachments/assets/32c5cd0c-b118-4404-a9e0-4a120a48389d" alt="Kong Services List" width="900"/></p>
3. Create a route for `pokemon-service`:
   A Route defines how requests are sent to a Service. Create a route that forwards requests with the `/pokemons` path to the `pokemon-service`.
    - Name: `pokemon-service-route`
    - Service: Select `pokemon-service`
    - Path: `/pokemons`
4. Create a route for `trainer-service`:
   Similarly, create a route that forwards requests with the `/trainers` path to the `trainer-service`.
    - Name: `trainer-service-route`
    - Service: Select `trainer-service`
    - Path: `/trainers`
    <p align="center"><img src="https://github.com/user-attachments/assets/e8758bf3-5218-4713-9e15-93c9d8ae0612" alt="Kong Routes List" width="900"/></p>
    
Your setup is now complete! Happy coding 🐞 You can begin making requests to the API Gateway (e.g., `http://localhost:8000/pokemons/get-data`).

## How To Modify The Service?
This guide outlines the development workflow for modifying a backend service, such as adding a new feature that requires dependency changes or database schema updates.

### Prerequisites
Before you begin, ensure you are working inside the specific service's directory (e.g., service-a/) and have activated the virtual environment.
```shell
cd service-a/
source .venv/bin/activate
uv sync
```

1. Managing Dependencies, 
When you need to add, update, or remove a Python package, follow this process.
    - Install a New Package:
    Use `uv` to add a new package. It will automatically update the `pyproject.toml` and `uv.lock` files.
    ```shell
    uv add "package-name"
    ```
    - Update requirements.txt:
     To ensure the requirements.txt file stays in sync for compatibility with other tools, regenerate it from the lock file.
    ```shell
    uv pip freeze > requirements.txt
    ```
2. Changing the Database Schema, 
This project uses Alembic to manage database migrations. The process is semi-automated.
    - Modify Your SQLAlchemy Models:
      First, make the desired changes directly in your Python code. For example, add a new column to a model in `app/models.py` or    create an entirely new model file.
    - Generate a Migration Script:
      Once your models are updated, run Alembic's autogenerate command. This will compare your SQLAlchemy models against the current state of the database and create a new migration script.
      ```Shell
      example
      alembic revision --autogenerate -m "Add description column to Pokemon model"
      ```
    This creates a new file inside `app/repository/migration/versions/.` You should review this file to ensure it accurately reflects your intended changes.
    > ℹ️ This template is configured to handle database upgrades automatically by simply run the application.
 
3. Running the Service
    ```
    python main.py
    ```
    Firstly the service will detect and apply any pending Alembic migrations on startup before the application begins serving requests, then your database schema is now up-to-date with your models, and the service is running with your latest code changes.
