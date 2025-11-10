import boto3
import json

class BedrockLLM:
    def __init__(self, model_id="amazon.nova-lite-v1:0", region="us-east-1"):
        self.client = boto3.client(service_name="bedrock-runtime", region_name=region)
        self.model_id = model_id

    def generate(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """Send a prompt to the Bedrock model and return the response text."""

        body = [
                {"role": "user", "content": [{"text": prompt}], }
        ]

        response = self.client.converse(
                modelId = self.model_id,
                messages = body,
                inferenceConfig = { "maxTokens": max_tokens, "temperature": temperature}
        )

        response_body = response["output"]["message"]##json.loads(response["body"].read())
        return response_body["content"][0]["text"]

