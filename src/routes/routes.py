from pathlib import Path

from fastapi import APIRouter, Form, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.controller.controller import StandardController
from src.models.models import StandardModel
from src.schemas.input_schema import StandardInputSchema
from src.schemas.response_schema import StandardResponseSchema, standard_response_examples

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates/"

myresource_router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# USUAL ROUTES

@myresource_router.post(
    "/api/standard_route_post",
    description="change data",
    status_code=200,
    response_model=StandardResponseSchema,
    responses=standard_response_examples
)
async def generate_standard_content(
        request_data: StandardInputSchema
):
    controller_obj = StandardController(
        standard_model=StandardModel(
            user_id="Anne",
            text=request_data.input

        ))
    await controller_obj.initialize_standard_controller()

    return {"result": controller_obj.standard_model.result}


# HTML ROUTES
# load html file
@myresource_router.get("/api/translate", response_class=HTMLResponse)
async def get_standard_data(request: Request):
    return templates.TemplateResponse(
        "lexilinker.html",
        context={"request": request, "result": ""}
    )


# fill html file with data
@myresource_router.post("/api/translate", response_class=HTMLResponse)
async def post_standard_data(request: Request, text: str = Form(...)):
    controller_obj = StandardController(
        standard_model=StandardModel(
            user_id="Anne",
            text=text

        ))
    await controller_obj.initialize_standard_controller()

    return templates.TemplateResponse(
        "lexilinker.html",
        context={"request": request, "result": controller_obj.standard_model.result}
    )


