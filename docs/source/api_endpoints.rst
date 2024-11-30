.. _api_endpoints:

API Endpoints
==============

The CookieBaker-AI project exposes several REST API endpoints for interaction with the AI system.

Response Endpoint
------------------

.. http:post:: /webhook/response

   Main endpoint for generating AI responses.

   **Parameters**

   * **prompt** (*string*) -- The user's input text prompt
   * **chat_id** (*string*) -- Unique identifier for the chat session
   * **client_name** (*string*) -- Name of the client making the request
   * **media** (*string*) -- URL pointing to a media file for multimodal analysis. Use empty string if no media is provided.

   **Example Request**::

      POST /response
      {
          "prompt": "What's in this image?",
          "chat_id": "chat123",
          "client_name": "web_client",
          "sfw": true,
          "sender_name": "Felipe Catapano",
          "media": "https://example.com/image.jpg"
      }

   **Example Response**::

      {
          "response": "What a beautiful cat!",
          "command": ""
      }

Commands Management
--------------------

.. http:post:: /webhook/commands

   Sets up available commands for a specific client.

   **Parameters**

   * **client_name** (*string*) -- Name of the client
   * **commands** (*object*) -- JSON object containing command definitions

   **Example Request**::

      POST /set_commands
      {
          "client_name": "web_client",
          "commands": {
              "command1": "description1",
              "command2": "description2"
          }
      }

.. http:get:: /webhook/commands

   Retrieves available commands for a specific client.

   **Parameters**

   * **client_name** (*string*) -- Name of the client

   **Example Request**::

      GET /get_commands?client_name=web_client

Logs Endpoints
---------------

.. http:get:: /webhook/logs/error

   Retrieves error logs for a specific client.

   **Parameters**

   * **client_name** (*string*) -- Name of the client

   **Example Request**::

      GET /logs/error?client_name=web_client

.. http:get:: /webhook/logs/metadata

   Retrieves logs of requests from a specific client.

   **Parameters**

   * **client_name** (*string*) -- Name of the client

   **Example Request**::

      GET /logs/metadata?client_name=web_client

.. http:get:: /webhook/logs/media

   Retrieves logs of text descriptions extracted from media files using the multimodal model.

   **Parameters**

   * **client_name** (*string*) -- Name of the client

   **Example Request**::

      GET /logs/media?client_name=web_client

.. http:get:: /webhook/logs/chat

   Retrieves logs of AI responses for a specific client.

   **Parameters**

   * **client_name** (*string*) -- Name of the client

   **Example Request**::

      GET /logs/chat?client_name=web_client

Monitoring Endpoints
---------------------

.. http:get:: /healthz

   Health check endpoint to verify service status.

   **Example Response**::

      {
          "status": "ok"
      }

.. http:get:: /metrics

   Provides hardware-software metrics for monitoring and testing purposes.

   **Example Response**::

    {
        # HELP process_cpu_user_seconds_total Total user CPU time spent in seconds.
        # TYPE process_cpu_user_seconds_total counter
        n8n_process_cpu_user_seconds_total 79.260337

        # HELP process_cpu_system_seconds_total Total system CPU time spent in seconds.
        # TYPE process_cpu_system_seconds_total counter
        n8n_process_cpu_system_seconds_total 24.728905

        # HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
        # TYPE process_cpu_seconds_total counter
        n8n_process_cpu_seconds_total 103.98924199999999

        ...
    }

Database Schema
----------------

The API uses two main tables for data persistence:

**client_commands**
    Stores command configurations for each client
    
    * id (SERIAL PRIMARY KEY)
    * client_name (VARCHAR)
    * client_commands (JSONB)

**logs**
    Stores interaction logs
    
    * id (SERIAL PRIMARY KEY)
    * client_name (VARCHAR)
    * chat_id (VARCHAR)
    * log_type (VARCHAR)
    * log_data (JSONB)

