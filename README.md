# CookieBaker-AI

## Project outline:

- Langchain app, self-hosted using LangServe
- Used by Cookiebot and Dynamo projects to act as the “brain” for natural language capabilities (with inputs from users)
- For Cookiebot, it will be accessed across machines using internal IP addresses. For Dynamo, it will be accessed via the localhost
- Multimodal inputs, context-aware responses, online integration capabilities, instruction execution/system modification capabilities
- Parallelization and resource monitoring with Dask
- Design for on-premise environments, potentially resource-restricted. No data is stored/posted outside of the running device (internet is only used for querying complex models and searching the web)

### The pipeline/chain:

1) Media tokenization layer extracts information from media (if any)
2) Context tokenization layer extracts information from chat and user
3) Command extraction layer extracts commands from natural conversation messages (and assembles json if any)
4) Response layer uses main LLMs and previous outputs in the chain to generate response
5) Every layer contains error handling measures and can return error messages
6) Separate API routes for setting command dictionary and client metadata (as this only has to be done once)

### Media tokenization layer:

- According to text input, prompt multimodal model to extract relevant information from input audios, images and videos
- GIFs should be converted to videos for this
- Documents should NOT be supported as it is not the focus of the application and could be exploited for DOS attacks

### Context tokenization layer:

- Obtain session information for chat context window
- According to previous inputs, compile metadata, which contains: chat rules, welcome message, title, description, configs, registers, last N messages in chat and sender name, username and privilege
- List of available commands and client metadata are compiled together with the metadata. The client is responsible for setting this information in the API

### Command extraction layer:

- Usage of embeddings to separate prompts that contain commands from prompts that are conversation-only
- If it does contain command(s), parse enforcing json schema using available relevant information and dictionary of available commands with their respective arguments
- If a valid command was detected but information is clearly missing, this should be reported in the output of this layer as well

### Response layer:

- SFW and special prompt configs affect the system input
- Join everything and query fine-tuned model accordingly, allowing access to tools for getting information from the web if relevant
- If classification layer returned a positive result, json for command(s) execution(s) will be added to the response
- Response is stored in chat context and returned
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
