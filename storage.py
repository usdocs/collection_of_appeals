'''Сохранение обращений в JSON-файлы на диске.'''

import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel

# Папка с файлами, создаётся рядом с проектом.
DATA_DIR = Path(__file__).resolve().parent / 'data'


def save_appeal(appeal: BaseModel) -> None:
    '''Сохранить обращение в отдельный JSON-файл.'''
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    path = DATA_DIR / f'appeal_{stamp}_{uuid4().hex[:8]}.json'
    payload = appeal.model_dump(mode='json')
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
