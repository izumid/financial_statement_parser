from fastapi import FastAPI
from controller import execute_task
import model

app = FastAPI()

@app.get("/")
async def root():
	return 204
	
@app.get("/healthCheck")
async def healthCheck():
	return 200
	
@app.post("/documentParser")
async def parsing(request: model.Request):
	try:
		if isinstance(request.id, str) and isinstance(request.base64, list):
			execute_task.apply_async(args=[request.id, request.base64])
		else:
			return({"error" f"[1.0] Error Type id is string? {isinstance(request.id, str)}. File is list? {isinstance(request.file, list)}"})
		
	except Exception as error:
		return {"error": f"[0.0] processing received file: {error}"}