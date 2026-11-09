'''Сервис сбора обращений абонентов на FastAPI + Pydantic.'''

import logging

from fastapi import FastAPI, HTTPException

from models import AppealRequest
from storage import save_appeal

logger = logging.getLogger(__name__)

app = FastAPI(
    title='Сбор обращений абонентов',
    description='Приём обращений с валидацией и сохранением в JSON.',
    version='1.0.0',
)


@app.post(
    '/appeal',
    response_model=AppealRequest,
    status_code=201,
    summary='Принять обращение абонента',
)
def create_appeal(appeal: AppealRequest) -> AppealRequest:
    '''Валидация через Pydantic и сохранение в JSON-файл.'''
    try:
        save_appeal(appeal)

    except OSError:
        logger.exception('не удалось сохранить обращение')
        raise HTTPException(
            status_code=500,
            detail='Не удалось сохранить обращение на диск',
        )

    return appeal
