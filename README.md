# CookieBaker-AI

## Project outline:

- n8n self-hosted workflow with containerized services
- All models run locally and all data is stored locally
- Used by Cookiebot and Dynamo projects to act as the “brain” for natural language capabilities (with inputs from users)
- For Cookiebot, it will be accessed across machines using internal IP addresses. For Dynamo, it will be accessed via the localhost
- Multimodal inputs, context-aware responses, online searching capabilities (if internet connection is available), command execution capabilities according to client-defined commands
- Workflow parallelization

### The pipeline/chain:

0) App receives input from client process, containing: sfw boolean, chat title, chat description, sender message (prompt), sender username/name, sender isadmin, and media (defaults to None)
1) Media tokenization layer extracts information from media [optional]
2) Conversation layer generates responses in natural language. It can also access web search tools and custom tools to retrieve chat and/or sender information, as well as the schema of available commands, set by the client
3) Separate API routes for setting command dictionary and client metadata (as this only has to be done once)

### Media tokenization layer:

- According to text input, prompt multimodal model to extract relevant information from input audios, images and videos
- Audio is converted to text (Whisper)
- Images are processed with OCR and visual-text question answering models (PadddleOCR and LLaVA-Phi3-Mini)
- Videos are separated into audio and first frame, then processed as audio and image
- GIFs are processed as videos
- Documents are NOT supported for security reasons

### Response layer:

- Model chosen based on SFW boolean (two fine-tuned Gemma2-2B)
- Join prompt with media tokenization layer output if any, and query model accordingly
- Postgres is used for chat-specific memory
- SerpAPI tool is used for web search if internet connection is available
- n8n sub-workflow tool is used for retrieving available commands schema and assembling json for command execution
- Response is stored in chat context and returned

## Endpoints:

- GET /response
- GET/POST/PUT /client_commands
- GET/POST/PUT /client_metadata
- GET /logs/error
- GET /logs/metadata
- GET /logs/media
- GET /logs/chat
