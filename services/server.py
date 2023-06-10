import uvicorn
from api import APP


if __name__ == "__main__":
    uvicorn.run(
        app="api.server:APP",
        #app="__name__:APP",
        host="0.0.0.0",
        port=5000,
        reload=True
    )
