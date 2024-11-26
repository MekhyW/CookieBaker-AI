# CookieBaker-AI

Conversational and command execution AI for Cookiebot and Dynamo projects

## Project outline:

- n8n self-hosted workflow with containerized services
- All models run locally and all data is stored locally
- Used by Cookiebot and Dynamo projects to act as the “brain” for natural language capabilities (with inputs from users)
- For Cookiebot, it will be accessed across machines using internal IP addresses. For Dynamo, it will be accessed via the localhost
- Multimodal inputs, context-aware responses, online searching capabilities (if internet connection is available), command execution capabilities according to client-defined commands
- Workflow parallelization

### The pipeline/chain:

0) App receives input from client process, containing: sfw boolean, sender message (prompt), sender username/name, and media (defaults to None)
1) Media tokenization step extracts information from media [optional]
2) Conversation step generates responses in natural language. It can also access web search tools and custom tools to retrieve chat and/or sender information, as well as the schema of available commands, set by the client
3) Separate API route for setting command dictionary (as this only has to be done once)

### Media tokenization step:

- At least for now, only images are supported. Text-to-speech and video-to-image should be done by the client before sending to the endpoint
- The image is first pre-processed with an OCR model (PaddleOCR)
- The image is then processed with a visual-text question answering model (LLaVA-Phi3-Mini)

### Response step:

- Model chosen based on SFW boolean (two fine-tuned Gemma2-2B)
- Join prompt with media tokenization layer output if any, and query model accordingly
- Postgres is used for chat-specific memory
- SerpAPI tool is used for web search if internet connection is available
- n8n sub-workflow tool is used for retrieving available commands schema and assembling json for command execution
- Response is stored in chat context and returned

## Endpoints:

- GET /response {client_name (string), chat_id (string), sfw (boolean), prompt (string), sender_name (string), sender_isadmin (boolean), media (string)}
- GET/POST/PUT /commands {unique_id (string, POST only), client_name (string), commands (json, POST and PUT only)}
- GET /logs/error {client_name (string)}
- GET /logs/metadata {client_name (string)}
- GET /logs/media {client_name (string)}
- GET /logs/chat {client_name (string)}
