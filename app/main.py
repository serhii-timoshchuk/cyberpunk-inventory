from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from configs.app_config import MAIN_PREFIX

from v1.app import v1_app
from v1.config import V1_PREFIX

app = FastAPI(openapi_url=f"{MAIN_PREFIX}/openapi.json",
              docs_url=f"{MAIN_PREFIX}/docs")

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.mount(f'{MAIN_PREFIX}{V1_PREFIX}', v1_app)


@app.get('/', include_in_schema=False)
def redirect_to_main_version_doc_from_root():
    return RedirectResponse(f'{MAIN_PREFIX}{V1_PREFIX}/docs')


@app.get(f'{MAIN_PREFIX}/', include_in_schema=False)
def redirect_to_main_version_doc_from_main_prefix():
    return RedirectResponse(f'{MAIN_PREFIX}{V1_PREFIX}/docs')
