from functools import lru_cache
import json
import app_config
import logging
from logging import config
from fastapi import FastAPI, Depends, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError, ValidationError, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import string
import sys
import time
import uvicorn

import ip.routes_items



sys.dont_write_bytecode = True

cfg = app_config.get_settings()
#config.dictConfig(cfg.log_config)
#logger = logging.getLogger(__name__)


app = FastAPI(
    title = 'Sherlog Nftables API',
    license_info={
        'name': 'Apache 2.0',
        'url' : 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
    description = cfg.description,
    version = '0.8.2',
)

app.include_router(ip.routes_items.router, prefix="/ip", tags=['IP'])


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}

    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


'''
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        logger.info(f"request_path={request.url}, request_headers={request.headers}")
        start_time = time.time()
    
        response = await call_next(request)
    
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        #logger.info(f"status_code={response.status_code}, headers={response.headers}, resp_content={response.content}")
    
        return response
    except Exception as e:
        logger.error('Failed write to log: '+ str(e))
'''




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
