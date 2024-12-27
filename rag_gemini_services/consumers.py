import json
from channels.generic.websocket import AsyncWebsocketConsumer
from utils.gemini_agent.agent_v2 import GeminiLLMChain, GeminiRetrievalQA

gemini_llm_chain = GeminiLLMChain()
gemini_retrieval_qa = GeminiRetrievalQA()
print("Done loading Gemini Agent")

class GeminiChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.send(text_data=json.dumps({"message": "connected"}))

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', None)
        content = message.get('content', None)
        chat_mode = message.get('mode', None)
        attachments = text_data_json.get('attachments', None)
        # Xử lý khác nhau dựa vào có attachment hay không
        if chat_mode == "rag":
            response = gemini_retrieval_qa.generate_answer(content, attachments)
        else:
            response = gemini_llm_chain.generate_answer(content)
        

        print(f"Response: {response}, type: {type(response)}")  
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'response': response
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        response = event['response']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': response
        }))
