Setup Workflow
==============

The docker compose file is the easiest way to get started. It will install all the necessary services and dependencies to run the workflow. The necessary models are already published on Ollama and can be pulled at scale.

Core Services
--------------

1. **PostgreSQL Database (postgres)**

   - Persistent storage for workflow data

   - Runs on port 5432

   - Automatically initializes required tables (using the script ``create_tables.sql``)

2. **n8n Workflow Engine**

   - Two containers:

        - ``n8n-import``: Imports initial workflows and credentials
        - ``n8n``: Main workflow engine running on port 5678

   - Connects to PostgreSQL for data storage
   - Stores workflows in persistent volume

3. **Ollama Model Server**

   - Supports both CPU and GPU configurations

   - Runs on port 11434

   - Automatically pulls required models:

        - ``llava-phi3``
        - ``MekhyW/cookiebaker-sfw``
        - ``MekhyW/cookiebaker-nsfw``

Configuration
--------------

The system uses Docker profiles to manage different hardware configurations:

.. code-block:: bash

    # For CPU-only deployment
    docker compose --profile cpu up -d

    # For NVIDIA GPU deployment
    docker compose --profile gpu-nvidia up -d

Key Components
---------------

Here are the key sections of the docker-compose.yml file:

.. code-block:: yaml

    # Volume definitions for persistent storage
    volumes:
      n8n_storage:        # Stores n8n data
      postgres_storage:    # Stores database data
      ollama_storage:     # Stores model data

    # Network configuration
    networks:
      demo:               # Internal network for service communication

The services are configured with health checks and dependencies to ensure proper startup order:

.. code-block:: yaml

    services:
      postgres:
        # ... configuration ...
        healthcheck:
          test: ['CMD-SHELL', 'pg_isready ...']
          interval: 5s
          timeout: 5s
          retries: 10

      n8n:
        # ... configuration ...
        depends_on:
          postgres:
            condition: service_healthy
          n8n-import:
            condition: service_completed_successfully

Environment Variables
----------------------

The following environment variables need to be set:

- ``POSTGRES_USER``: Database username (default: ``root``)

- ``POSTGRES_PASSWORD``: Database password (default: ``password``)

- ``POSTGRES_DB``: Database name (default: ``n8n``)

- ``N8N_ENCRYPTION_KEY``: Encryption key for n8n (default: ``super-secret-key``)

- ``N8N_USER_MANAGEMENT_JWT_SECRET``: JWT secret for n8n user management (default: ``even-more-secret``)

These can be set in a ``.env`` file in the same directory as the docker-compose.yml file. 

.. warning::
   Change the defaults if you are going to expose the services to the public internet!

Getting Started
----------------

1. Clone the repository
2. Create a ``.env`` file with required variables
3. Start the services:

   .. code-block:: bash

       # For CPU deployment
       docker compose --profile cpu up -d

       # Or for GPU deployment
       docker compose --profile gpu-nvidia up -d

4. Access n8n at ``http://localhost:5678``
5. Import the ``CookieBaker_AI.json`` workflow into n8n

.. note::
   For completely automated/headless deployments, you can use the n8n CLI instead of the web interface, with minimal changes. Refer to the official documentation at https://docs.n8n.io/hosting/cli-commands/

