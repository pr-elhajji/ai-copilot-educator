

import os

from colorama import Fore, Style
from langchain_community.chat_models import ChatOllama



class OllamaProvider:

    def __init__(
        self,
        model,
        temperature,
        max_tokens,
        #base_url,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = self.get_llm_model()
        #self.base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")



    def get_llm_model(self):
        # Initializing the chat model
        base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        llm = ChatOllama( model="llama2",base_url=base_url, format="json" , temperature=0.55, max_tokens=2000)
            #self.model,
            #temperature=self.temperature,
            #max_tokens=self.max_tokens,
       # )

        return llm

    async def get_chat_response(self, messages, stream, websocket=None):
        if not stream:
            # Getting output from the model chain using ainvoke for asynchronous invoking
            output = await self.llm.ainvoke(messages)

            return output.content

        else:
            return await self.stream_response(messages, websocket)

    async def stream_response(self, messages, websocket=None):
        paragraph = ""
        response = ""

        # Streaming the response using the chain astream method from langchain
        async for chunk in self.llm.astream(messages):
            content = chunk.content
            if content is not None:
                response += content
                paragraph += content
                if "\n" in paragraph:
                    if websocket is not None:
                        await websocket.send_json({"type": "report", "output": paragraph})
                    else:
                        print(f"{Fore.GREEN}{paragraph}{Style.RESET_ALL}")
                    paragraph = ""
                    
        return response
