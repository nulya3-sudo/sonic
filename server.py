import asyncio, os, websockets

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            for c in list(clients):
                if c != ws:
                    try: await c.send(msg)
                    except: clients.discard(c)
    finally:
        clients.discard(ws)

async def main():
    port = int(os.environ.get("PORT", 8080))
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()

asyncio.run(main())