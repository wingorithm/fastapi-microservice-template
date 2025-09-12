<h1 align=center><strong>Fastapi Microservice Template</strong></h1>

A production-ready template to jumpstart your microservice projects using FastAPI. This repository provides a structured foundation inspired by real-world applications, so you can focus on building features instead of boilerplate.
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
you'll have 2 client entry endpoint

### 1st journey pokemon to trainer
client will ask our system to find random pokemon data follows by the possible trainer for it 
-> hit {gateway_url}/pokemons/get-data -> hit service-a -> hit service-b -> return to client  
//todo: gambar

![1st journey pokemon to trainer](https://github.com/user-attachments/assets/7840747a-933e-4ea2-bfa3-3645bd7633dd)

### 2nd journey trainer to pokemon
client will ask our system to find random trainer data follows by the possible pokemon to tame
client -> hit {gateway_url}/trainers/get-data -> hit service-b -> hit service-a -> return to client  
//todo: gambar

![2nd journey trainer to pokemon](https://github.com/user-attachments/assets/9ea6c7bf-ed16-4cd3-becd-87084908f007)


## How to Setup?
This project is now structured using multiple docker-compose files to separate the core infrastructure from the application services. This is the practice for managing different service lifecycles and environments.
```shell
├── docker-compose.yml           # Application services (service_a, service_b, etc.)
├── docker-compose.infra.yml     # Infrastructure (PostgreSQL, Consul, Registrator, Kong)
└── postgres-init/
    └── init-multi-db.sh         # bootstrap file for Postgre
```

### 1. start the infrastructure stack
```shell
docker-compose -f docker-compose.infra.yml up -d
```
ensure postgres, consul, kong, etc. to become healthy. otherwise try to restart specific container that still unhealthy.
> (ℹ️) special case for the kong-bootstrap it is expected to stop running after database bootstrapping finish.

### 2. check bootstrap result
there are some bootstrapping that are going to make
1. postgres db and schema, ensure this following db and schema are exist
```text
├── kong
    └── public
        └── 35 tables
├── microservice
    └──service_a
    └──service_b
```

### 3. Start the Application Services
```shell
docker-compose -f docker-compose.yml up -d
```
when every time service is starting... it will try to migrate the migrations using `alembic`. So table that we devine in code base will also created in the database.
before you can fully use the app endpoint, insert application's data in `postgres-init\example-data.sql`
> (ℹ️) DO NOT change version data in `*/app/repository/migration/versions/*.py`, if you need to change the migration follow instruction at section 'How To Modify The Code?'

### 4. Setup & Inspect Consul Service Registry
consul provide web UI to interact with Consul, enter the web UI go to `http://localhost:8500/`. Then on tab /services you may see something like below
> using UI is not weak, it not just easier, but help us reduce human error 😎
![WhatsApp Image 2025-09-07 at 18 21 59_b03df09b](https://github.com/user-attachments/assets/fbb27c7c-1ce9-4531-b7a6-3047721341b2)

don't forget to setup app config in consul kv - centralize configuration, you may also do it via UI
![WhatsApp Image 2025-09-12 at 11 54 40_dada0a7e](https://github.com/user-attachments/assets/1108ce91-7836-49e1-8a03-860b8f75cae0)


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
1. uv pip install -r requirements.txt

2. alembic revision --autogenerate -m "Create pokemons table" -> app/repository/migration/versions/xxxx_xxxx_table.py

3. run the service `python main.py` -> table created


