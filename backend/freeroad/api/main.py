from fastapi import FastAPI
from freeroad.api.routes import comment_route, post_route, user_route
from freeroad.api.openapi_tags import openapi_tags


app = FastAPI(
    title="Blog API",
    description="API backend do Blog com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Lázaro Eduardo", "email": "lazaro@exemplo.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
)


@app.get("/")
def ola():
    return {"olá": "fastapi"}


app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(post_route.router, prefix="/posts", tags=["Posts"])
app.include_router(comment_route.router, prefix="/comments", tags=["Comments"])
