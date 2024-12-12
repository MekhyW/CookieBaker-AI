What is this?
==============

CookieBaker is a project that aims to provide self-hosted and self-contained conversational and command execution intelligence for two other projects of mine: Cookiebot (a group chatbot for Telegram) and Dynamo (a wearable system with a voice assistant) but can be used in other projects as well.

A client application can use the provided API endpoints to send a list of commands it can execute, with their arguments and descriptions, and send user chat messages. These messages can include a URL to a media file (only images are supported at the moment) to be included as part of the prompt. CookieBaker can then generate natural language chat responses, as well as structured command intents according to the client-defined commands.

Additionally, the workflow logs all messages, responses, media captions and errors to the database, and provides API endpoints to access them for debugging and model observability.

Explanatory Video
-----------------

.. warning::
   The video uses outdated visuals, open the workflow in the browser to see the current state.

.. raw:: html

   <iframe width="800" height="450" src="https://www.youtube.com/embed/CdBSwl0_ISQ" allowfullscreen></iframe>

Services
---------

The project is containerized and uses the following services:

- **n8n**: A workflow automation tool that allows to create complex workflows by connecting different actions (endpoints) together. In this project, it is used to orchestrate the chat and command execution workflows.

- **Ollama**: An open-source, self-hosted tool for running large language models locally.

- **PostgreSQL**: A powerful, open-source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.

- **SerpAPI**: A tool that allows models to search the web for information. It is included in n8n as a tool node.

The following technologies were also used for development of the models:

- **DVC**: A version control system for machine learning projects.

- **Hugging Face**: A platform for machine learning and natural language processing research and development.

- **Weights & Biases**: A platform for experiment tracking, model observability and collaboration.

Pipeline Steps
---------------

1) App receives request from client process to set up list of commands available for execution

.. image:: _static/pipeline_1.png
   :alt: Pipeline step 1
   :width: 400
   :align: center

2) App receives request from client process to generate a response, including the necessary metadata. If the message contains a media URL, it is downloaded, resized (to prevent tokenization issues) and caption is generated using a multimodal model.

.. image:: _static/pipeline_2.png
   :alt: Pipeline step 2
   :width: 600
   :align: center

3) A model is chosen according to the SFW/NSFW boolean, and it is used to generate a response. The models have access to the history of the conversation of the corresponding chat_id, can search the web using SerpAPI if internet access is available, and can fetch the available commands according to the client-defined list. The responses are returned as webhook responses to the client and logged in the database.

.. image:: _static/pipeline_3.png
   :alt: Pipeline step 3
   :width: 800
   :align: center

4) If an error occurs at any point, it is logged in the database and a message is returned to the client.

.. image:: _static/pipeline_4.png
   :alt: Pipeline step 4
   :width: 400
   :align: center

5) All logs can be accessed using separate API endpoints provided by the project.

.. image:: _static/pipeline_5.png
   :alt: Pipeline step 5
   :width: 400
   :align: center


Models
-------

The project utilizes three specialized Large Language Models, all of which are now public and pulled automatically from the Ollama servers:

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :align: left

   * - Model
     - Description
   * - **Describer Model**
     - | **Purpose**: Generate captions for media in user messages
       | **Type**: Multimodal (image + text input)
       | **Base Model**: ``LLaVA-Phi3``
       | **Architecture**: Small LLaVa model fine-tuned from Phi 3 Mini 4k
       | **Performance**: Comparable to original LLaVA model
   * - **SFW Model**
     - | **Purpose**: Generate responses for Safe-For-Work chats
       | **Base Model**: ``Gemma2-2b-it-abliterated``
       | **Architecture**: Custom fine-tuned adapter + Gemma 2 (2B parameters)
       | **Note**: System messages implemented via user message prefixing
   * - **NSFW Model**
     - | **Purpose**: Generate responses for NSFW (18+) chats
       | **Base Model**: ``Gemma2-2b-it-abliterated``
       | **Architecture**: Same as SFW model with different adapter
       | **Difference**: Uses NSFW chat data for training
