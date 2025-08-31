#UNDER CONSTRUCTION (pls wait 🙏)
1. uv pip install -r requirements.txt

2. alembic revision --autogenerate -m "Create pokemons table" -> app/repository/migration/versions/xxxx_xxxx_table.py

3. run the service `python main.py` -> table created

apigateway : use KONG gateway own infrastructure not the KONG KONNECT

Multi-Compose File Setup Guide
This project is now structured using multiple docker-compose files to separate the core infrastructure from the application services. This is a best practice for managing different service lifecycles and environments.

File Structure
.
├── docker-compose.yml           # Application services (Kong, service_a, etc.)
├── docker-compose.infra.yml     # Infrastructure (PostgreSQL, Consul)
└── postgres-init/
    └── init-multi-db.sh

How It Works
docker-compose.infra.yml: This file defines and creates the "slow-moving" parts of your stack: the database (postgres) and service discovery (consul). It is also responsible for creating the shared network (microservices-net) and the data volume (postgres_data).

docker-compose.yml: This file defines your applications. It declares the microservices-net network as external: true. This is a critical instruction that tells Docker Compose, "Don't create this network; just connect my services to the one that already exists."

This separation allows you to tear down and restart your application services without affecting your running database.

How to Run
You must start the infrastructure stack first, as the application stack depends on the network it creates.

Start the Infrastructure:
Open your terminal and run:

docker-compose -f docker-compose.infra.yml up -d

Wait for the services (especially postgres) to become healthy.

Start the Application Services:
In the same terminal, run:

docker-compose -f docker-compose.yml up -d

Starting Everything at Once
You can also start both stacks with a single command by passing multiple -f flags. The order matters; Docker Compose processes them sequentially.

docker-compose -f docker-compose.infra.yml -f docker-compose.yml up -d

How to Stop
To stop everything, you can run the same command with down:

docker-compose -f docker-compose.infra.yml -f docker-compose.yml down
