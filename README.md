# CookieBaker-AI

## Project outline:

- Langchain app, self-hosted using LangServe
- All models run locally and all data is stored locally
- Used by Cookiebot and Dynamo projects to act as the “brain” for natural language capabilities (with inputs from users)
- For Cookiebot, it will be accessed across machines using internal IP addresses. For Dynamo, it will be accessed via the localhost
- Multimodal inputs, context-aware responses, online searching capabilities (if internet connection is available), command execution capabilities according to client-defined commands
- Parallelization and resource monitoring with Dask
- Design for on-premise environments, potentially resource-restricted. No data is stored/posted outside of the running device (internet is only used for querying complex models and searching the web)

### The pipeline/chain:

0) App receives input from client process, containing: chat configs, chat title, chat description, sender message (prompt), sender name, sender username, sender isadminprompt, and media [optional]
1) Media tokenization layer extracts information from media [optional]
2) Command extraction layer extracts commands from natural conversation messages, considering list of available commands (and assembles json if any)
3) Response layer uses main LLMs and previous outputs in the chain to generate response. It can also access web search tools and custom tools to retrieve chat and/or sender information
4) Every layer contains error handling measures and can return error messages
5) Separate API routes for setting command dictionary and client metadata (as this only has to be done once)

### Media tokenization layer:

- According to text input, prompt multimodal model to extract relevant information from input audios, images and videos
- Audio is converted to text using a speech-to-text model
- Images are processed using CLIP and OCR
- Videos are separated into audio and first frame, then processed as audio and image
- GIFs are processed as videos
- Documents are NOT supported as it is not the focus of the application and could be exploited for DOS attacks

### Command extraction layer:

- Decide if prompt (+ media tokenization layer output if any) contains commands or is conversation-only, using the previously set list of available commands
- If it does contain command(s), parse enforcing json schema using available relevant information and dictionary of available commands with their respective arguments
- If a valid command was detected but information is clearly missing, this should be reported in the output of this layer as well

### Response layer:

- Model chosen based on SFW boolean (and affected by chat language and context if available)
- Join everything and query fine-tuned model accordingly, allowing access to tools for getting information from the web or user or chat if relevant
- If classification layer returned a positive result, json for command(s) execution(s) will be added to the response
- Response is stored in chat context and returned, including command execution json if any
- The client is responsible for reporting failure/success of command executions back to the user

## Installation

Install the LangChain CLI if you haven't yet

```bash
pip install -U langchain-cli
```

## Adding packages

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```
