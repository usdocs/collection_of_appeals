'''Pydantic-модели сервиса сбора обращений абонентов.'''

import re
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator

# Фамилия/имя: заглавная буква кириллицы, дальше — только строчные буквы.
CYRILLIC_NAME_RE = re.compile(r'^[А-ЯЁ][а-яё]+$')

# Телефон: +7XXXXXXXXXX или 8XXXXXXXXXX.
PHONE_RE = re.compile(r'^\+?[78]\d{10}$')

# E-mail: простой, но строгий формат.
EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class AppealReason(str, Enum):
    '''Перечисление причин обращения'''

    NO_NETWORK = 'нет доступа к сети'
    PHONE_NOT_WORKING = 'не работает телефон'
    NO_EMAILS = 'не приходят письма'


class AppealBase(BaseModel):
    '''Базовые атрибуты обращения абонента.'''

    last_name: str = Field(
        ...,
        pattern=CYRILLIC_NAME_RE,
        description='Фамилия: с заглавной буквы, только буквы кириллицы',
        examples=['Иванов'],
    )
    first_name: str = Field(
        ...,
        pattern=CYRILLIC_NAME_RE,
        description='Имя: с заглавной буквы, только буквы кириллицы',
        examples=['Иван'],
    )
    birth_date: date = Field(
        ...,
        description='Дата рождения в формате ГГГГ-ММ-ДД',
        examples=['1990-05-15'],
    )
    phone: str = Field(
        ...,
        pattern=PHONE_RE,
        description='Номер телефона: +7XXXXXXXXXX или 8XXXXXXXXXX',
        examples=['+79001234567'],
    )
    email: str = Field(
        ...,
        pattern=EMAIL_RE,
        description='E-mail',
        examples=['ivanov@example.com'],
    )

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        '''Дата рождения не может быть в будущем.'''
        if value > date.today():
            raise ValueError('дата рождения не может быть в будущем')

        return value


class AppealRequest(AppealBase):
    '''
    Обращение абонента: базовые атрибуты, одна или несколько причин
    обращения (``reasons``) и дата/время обнаружения проблемы.
    '''

    reasons: list[AppealReason] = Field(
        ...,
        min_length=1,
        description='Одна или несколько причин обращения',
        examples=[['нет доступа к сети']],
    )
    detected_at: datetime = Field(
        ...,
        description='Дата и время обнаружения проблемы (ISO 8601)',
        examples=['2026-11-08T14:30:00'],
    )

    @field_validator('reasons')
    @classmethod
    def validate_reasons(
        cls,
        values: list[AppealReason],
    ) -> list[AppealReason]:
        '''Причины обращения не должны повторяться.'''
        if len(set(values)) != len(values):
            raise ValueError('причины обращения не должны повторяться')

        return values

    @field_validator('detected_at')
    @classmethod
    def validate_detected_at(
        cls,
        value: datetime,
    ) -> datetime:
        '''Проблема не может быть обнаружена в будущем.'''
        if value > datetime.now():
            raise ValueError(
                'дата и время обнаружения проблемы не могут быть в будущем'
            )

        return value
