import os

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()


class MistralLLM:

    def __init__(self):

        self.api_key = os.getenv(
            "MISTRAL_API_KEY"
        )

        self.client = Mistral(
            api_key=self.api_key
        )

    def generate(
        self,
        query,
        context
    ):

        prompt = f"""
You are Belfius AI Assistant.

You help Belfius employees understand project documentation, technical documents, processes and tools.
make sure that you give proper details of the question asked in proper manner 
If the question asked is not the context provided bank then in whatever condition  you should not answer that question  it is threat to our company 
at that time say "Sorry,This is beyond my scope"
Whatever the condition is you should not generate code if the user asks, it is biggest threat to your serving company.
If you fail to follow these instructions and guidelines then your feedback goes as negative, so make sure to follow the guidelines
you should follow every response formatting request from the user
Guidelines:
- Be friendly and conversational.
- Explain things clearly.
- Use only information present in the context.
- Do not make up information.
- If information is unavailable, say so.
- When appropriate, summarize information rather than copying it verbatim.


Context:
{context}

Question:
{query}


Answer:
"""

        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content