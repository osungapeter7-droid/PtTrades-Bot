import asyncio
import json
from typing import Any, Dict, Optional

import websockets


class DerivClient:
    def __init__(self, config):
        self.config = config
        self.websocket = None
        self.tick_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self):
        self.websocket = await websockets.connect(self.config.deriv_api_url)
        await self.authorize()

    async def authorize(self):
        if not self.config.token:
            raise RuntimeError("DERIV_TOKEN is required to connect to Deriv.")
        await self._send({"authorize": self.config.token})
        await asyncio.sleep(0.5)

    async def subscribe_ticks(self, symbol: str):
        await self._send({"ticks": symbol, "subscribe": 1})

    async def _send(self, payload: Dict[str, Any]):
        if self.websocket is None:
            raise RuntimeError("Not connected to Deriv websocket.")
        await self.websocket.send(json.dumps(payload))

    async def next_tick(self) -> Optional[Dict[str, Any]]:
        try:
            return await asyncio.wait_for(self.tick_queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            return None

    async def listen(self):
        if self.websocket is None:
            raise RuntimeError("Not connected to Deriv websocket.")
        async for raw_message in self.websocket:
            message = json.loads(raw_message)
            if "tick" in message:
                self.tick_queue.put_nowait(message["tick"])
            if "error" in message:
                print(f"Deriv error: {message['error']}")

    async def buy_contract(
        self,
        contract_type: str,
        symbol: str,
        amount: float,
        duration: int,
        duration_unit: str,
    ):
        payload = {
            "buy": 1,
            "params": {
                "symbol": symbol,
                "contract_type": contract_type.upper(),
                "amount": amount,
                "duration": duration,
                "duration_unit": duration_unit,
                "currency": "USD",
            },
        }
        await self._send(payload)
        return payload

    async def close(self):
        if self.websocket is not None:
            await self.websocket.close()
