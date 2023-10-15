from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter()

@router.get('/data')
def get_data():
    data = {
        "key": "value",
        "number": 123,
        "array": [1, 2, 3],
        "nested": {
            "name": "example",
            "boolean": True
        }
    }
    return JSONResponse(content=data)

# Define a route for the root URL ("/")
@app.get('/')
def root():
    return {"message": "Welcome to the root endpoint"}

# Define a route for the favicon.ico file
@app.get('/favicon.ico')
def favicon():
    return JSONResponse(content={}, status_code=204)  # Return an empty response with status code 204

app.include_router(router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
