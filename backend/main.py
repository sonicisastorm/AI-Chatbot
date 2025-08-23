import os
import json
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import boto3
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clients
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

bedrock_agent_client = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query", "")

    try:
        # Query the Knowledge Base
        knowledge_base_response = bedrock_agent_client.retrieve(
            knowledgeBaseId="JGMPKF6VEI",  
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "vectorSearchConfiguration": {"numberOfResults": 3}
            }
        )

        # Extract context from retrieved docs
        context = "\n".join(
            [item["content"]["text"] for item in knowledge_base_response.get("retrievalResults", [])]
        )

        response = bedrock_client.invoke_model_with_response_stream(
            modelId=os.getenv("MODEL_ID"), 
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "system": "You are a helpful assistant.",
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": f"{context}\n{query}"}]
                    }
                ]
            }),
            contentType="application/json",
            accept="application/json"
        )

        # Stream back response
        stream_body = response.get("body")

        def event_generator():
            try:
                for event in stream_body:
                    chunk = event.get("chunk")
                    if not chunk:
                        continue

                    decoded = json.loads(chunk.get("bytes").decode("utf-8"))
                    if decoded.get("type") == "content_block_delta":
                        delta = decoded.get("delta", {})
                        text = delta.get("text", "")
                        if text:
                            yield text
            except Exception as e:
                logger.error(f"Streaming error: {e}")
                yield f"[ERROR]: {str(e)}"

        return StreamingResponse(event_generator(), media_type="text/plain")

    except Exception as e:
        logger.error(f"Bedrock error: {e}")
        return {"error": str(e)}