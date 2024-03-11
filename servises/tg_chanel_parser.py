from telethon import TelegramClient


class GetTGMessageChanel:
    def __init__(self, session_name, api_id, api_hash):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = None
        self.channel = None
        self.tg_client = None
        self.message = None
        self.message_lst = None

    async def connect_tg_client(self):
        """Connect to telegram account"""
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        await self.client.start()

    async def connect_tg_channel(self):
        """Connect to telegram chanel"""
        self.channel = await self.client.get_entity(-1001499158008)

    async def get_message(self):
        """Get latest message from tg chanel"""
        messages = await self.client.get_messages(self.channel, limit=1)

        self.message = messages[0].text
        print(self.message)
        self.message_lst = self.message.split()

        return self.message
