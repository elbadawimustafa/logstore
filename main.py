from fastapi import FastAPI, Request, Response, status
from svc import LogService, NotFound

app = FastAPI()
service = LogService()

@app.get("/logs/{eventID}")
async def getLog(eventID: str, response: Response):
    try:
        log = service.getLog(eventID)
    except NotFound as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": str(e)}
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error", "internal_server_error"}

    return log

@app.post("/logs", status_code=status.HTTP_200_OK)
async def insertLog(req: Request):
    res = []
    body = await req.json()

    for log in body:
        out = {"event_id": log["event_id"]}
        try:
            service.putLog(log)
            out["success"] = True
        except Exception as e:
            out["success"] = False
            out["error"] = str(e)
        finally:
            res.append(out)

    return res
