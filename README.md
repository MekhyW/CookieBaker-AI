# CookieBaker-AI (WIP)

## Project outline:

- n8n self-hosted workflow with containerized services
- All models run locally and all data is stored locally
- Used by Cookiebot and Dynamo projects to act as the “brain” for natural language capabilities (with inputs from users)
- For Cookiebot, it will be accessed across machines using internal IP addresses. For Dynamo, it will be accessed via the localhost
- Multimodal inputs, context-aware responses, online searching capabilities (if internet connection is available), command execution capabilities according to client-defined commands
- Workflow parallelization
- Design for on-premise environments, potentially resource-restricted. No data is stored/posted outside of the running device (internet is only used for querying complex models and searching the web)

### The pipeline/chain:

0) App receives input from client process, containing: sfw boolean, chat title, chat description, sender message (prompt), sender username/name, sender isadmin, and media (defaults to None)
1) Media tokenization layer extracts information from media [optional]
2) Selection layer decides whether the incoming prompt is a command or a conversation message, and chooses between the command extraction layer and the response layer
3) Command extraction layer extracts commands from messages classified as command intents, considering list of available commands, then assembles json. It can also access web search tools and custom tools to retrieve chat and/or sender information
4) Conversation layer generates responses in natural language. It can also access web search tools and custom tools to retrieve chat and/or sender information
5) Separate API routes for setting command dictionary and client metadata (as this only has to be done once)

### Media tokenization layer:

- According to text input, prompt multimodal model to extract relevant information from input audios, images and videos
- Audio is converted to text (Whisper)
- Images are processed with OCR and visual-text question answering models (PadddleOCR and LLaVA-Phi3-Mini)
- Videos are separated into audio and first frame, then processed as audio and image
- GIFs are processed as videos
- Documents are NOT supported for security reasons

### Selection layer:

- Decide if prompt contains commands or is conversation-only (fine-tuned TinyBERT)
- If is is a command, pass it to the command extraction layer. If it is conversation-only, pass it to the response layer instead

### Command extraction layer:

- Extract commands from the prompt, considering the list of available commands
- Assemble json for command execution, with the necessary arguments, allowing access to tools for getting information from the web or user or chat if relevant
- If a valid command was detected but information is clearly missing, this should be reported in the output of this layer as well

### Response layer:

- Model chosen based on SFW boolean (two fine-tuned Gemma2-2B)
- Join prompt with media tokenization layer output if any, and query model accordingly, allowing access to tools for getting information from the web or user or chat if relevant
- Response is stored in chat context and returned


## Endpoints:

- GET /response
- POST/PUT/DELETE /commands
- POST/PUT/DELETE /client_metadata
- GET /speech_to_text
- GET /text_to_speech
- GET /logs/error
- GET /logs/metadata
- GET /logs/media
- GET /logs/responses
