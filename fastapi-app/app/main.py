from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta

app = FastAPI(title="Indicators API")

@app.get("/healthz")
def health():
    return {"status": "ok"}

# 샘플: /stocks/top-movers (목데이터)
class Macd(BaseModel):
    value: float | None = None
    signal: float | None = None
    hist: float | None = None

class Indicators(BaseModel):
    bbPosition: float | None = None
    macd: Macd | None = None
    rsi: float | None = None

class TopMoverItem(BaseModel):
    symbol: str
    name: str
    changePct5d: float
    absChange5d: float
    close: float
    volume: int
    volumeRatio5d: float | None = None
    indicators: Indicators | None = None
    sparkline: list[float] | None = None

class TopMoversResponse(BaseModel):
    generatedAt: str
    window: str
    direction: str
    items: list[TopMoverItem]

@app.get("/stocks/top-movers", response_model=TopMoversResponse)
def top_movers(
        window: str = Query("5d"),
        direction: str = Query("up"),       # up | down
        limit: int = Query(10, ge=1, le=50),
        include: str | None = None,
        sparkline: bool = True
):
    now = datetime.now(timezone(timedelta(hours=9))).isoformat()
    sign = 1 if direction == "up" else -1
    items = []
    for i in range(limit):
        pct = round((15.23 - i*0.7) * sign, 2)
        items.append(TopMoverItem(
            symbol=f"TEST{i}",
            name=f"테스트{i}",
            changePct5d=pct,
            absChange5d=1200.0 * sign,
            close=10000.0 + i*10,
            volume=3000000 + i*1000,
            volumeRatio5d=1.8,
            indicators=Indicators(
                bbPosition=0.8 if direction=="up" else 0.2,
                macd=Macd(value=1.2*sign, signal=0.9*sign, hist=0.3*sign),
                rsi=68.0 if direction=="up" else 32.0
            ),
            sparkline=[9800+i*3, 9850+i*3, 9900+i*3, 9970+i*3, 10000+i*3] if sparkline else None
        ))
    return TopMoversResponse(generatedAt=now, window=window, direction=direction, items=items)
