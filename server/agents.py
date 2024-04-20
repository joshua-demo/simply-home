from uagents import Agent, Context, Model


class TestRequest(Model):
    message: str


class Response(Model):
    text: str


orchestrator = Agent(
   name="orchestrator", 
   port=8001, # 8000 is the server
   seed="orchestrator recovery phrase",
   endpoint=["http://localhost:8001/submit"],
)


@orchestrator.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {orchestrator.name}")
    ctx.logger.info(f"With address: {orchestrator.address}")
    ctx.logger.info(f"And wallet address: {orchestrator.wallet.address()}")


@orchestrator.on_query(model=TestRequest, replies={Response})
async def query_handler(ctx: Context, sender: str, _query: TestRequest):
    ctx.logger.info("Query received")
    try:
        # do something here
        await ctx.send(sender, Response(text="success"))
    except Exception:
        await ctx.send(sender, Response(text="fail"))


if __name__ == "__main__":
    orchestrator.run()