up:
	@echo "Starting FastAPI app ..."
	cd app && uvicorn main:app --reload