from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/alerts")
async def receive_alerts(request: Request):
    alerts = await request.json()
    print("Received alerts:")
    print(alerts)
    return {"status": "received"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
