class SessionAgent:
    def __init__(self, agent):
        self.agent = agent
        self.total = 0

    async def run(self, *args, **kwargs):
        result = await self.agent.run(*args, **kwargs)
        self.total += result.usage.total_tokens
        return result
