from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
async def example_endpoint():
    return {"message": "This is an example endpoint"}

# Additional endpoints can be defined here

# The router is then included in the main app instance in server.py
