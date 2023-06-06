# import requests
from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.start_question import start
from keyboards.chose_date import chose_date
from keyboards.chose_start_end import chose_start_end, chose_finish, chose_hard_from, chose_hard_to
from datetime import date, datetime

router = Router()  # [1]
API_KEY = 'bcbedf3a-ed56-419c-b2f6-0f6295f7cee5'


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    await message.answer(
        "Выберите транспорт:",
        reply_markup=start()
    )


data_for_send_req = {
    'transport_type': '',
    'start_point': '',
    'end_point': '',
    'current_date_str': '',
    'toggle': False
}


# вспомогательные функции


async def req_marshrut(transport_type, start_point, end_point, current_date_str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                'https://api.rasp.yandex.net/v3.0/search/' +
                f'?apikey={API_KEY}' +
                f'&transport_types={transport_type}' +
                '&format=json' +
                f'&from={start_point}' +
                f'&to={end_point}' +
                '&lang=ru_RU' +
                '&page=1' +
                f'&date={current_date_str}'
        ) as response:
            print('response')
            data = await response.json()
            print(data)
            return data


# выбор транспорта


@router.message(Text(text="самолет", ignore_case=True))
async def answer_plane(message: Message):
    await message.answer(
        f"Вы выбрали {message.text}",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Text(text="поезд", ignore_case=True))
async def answer_train(message: Message):
    await message.answer(
        f"Вы выбрали {message.text}",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Text(text="электричка", ignore_case=True))
async def answer_suburban(message: Message):
    data_for_send_req['transport_type'] = 'suburban'
    await message.answer(
        f"Вы выбрали {message.text[0:-1] + 'у'}. Теперь выберите дату",
        reply_markup=chose_date()
    )


@router.message(Text(text="автобус", ignore_case=True))
async def answer_bus(message: Message):
    await message.answer(
        f"Вы выбрали {message.text}",
        reply_markup=ReplyKeyboardRemove()
    )


# выбор даты

@router.message(Text(text="сегодня", ignore_case=True))
async def answer_date(message: Message):
    current_date = date.today().isoformat()
    # current_date_str = f'{current_date.year}-{current_date.month}-{current_date.day}'
    data_for_send_req['current_date_str'] = current_date
    await message.answer(
        f"Сегодня. Выберите место отправление и место прибытия:",
        reply_markup=chose_start_end()
    )


# выбор откуда и куда


@router.message(Text(text="откуда", ignore_case=True))
async def answer_from(message: Message):
    print(data_for_send_req)
    await message.answer(
        f"Введите точку отправления:",
        reply_markup=chose_hard_from()
    )


@router.message(Text(text="куда", ignore_case=True))
async def answer_to(message: Message):
    print(data_for_send_req)
    await message.answer(
        f"Введите точку прибытия:",
        reply_markup=chose_hard_to()
    )


# обработка кнопки назад в финальном слайде
@router.message(Text(text="назад", ignore_case=True))
async def back(message: Message):
    await message.answer("Сегодня. Выберите место отправление и место прибытия:", reply_markup=chose_start_end())


# обработка финального слайда - поиск
@router.message(Text(text="поиск", ignore_case=True))
async def set_search(message: Message):
    data = {k: v for k, v in data_for_send_req.items() if k != 'toggle'}
    print(data)
    res = await req_marshrut(
        data_for_send_req['transport_type'],
        data_for_send_req['start_point'],
        data_for_send_req['end_point'],
        data_for_send_req['current_date_str']
    )

    response_title = f'Дата расписания - {res["search"]["date"]}\n' \
                     f'Отправление - {res["search"]["from"]["title"]}\n' \
                     f'Прибытие - {res["search"]["to"]["title"]}\n'

    out = [f'{datetime.fromisoformat(s["departure"]).strftime("%H:%M")} : {s["thread"]["title"]}' for s in
           res["segments"]]
    print(f'out - {out}')
    response_body = f'Время  Название электрички \n'
    for o in out:
        response_body = response_body + o + '\n'
    await message.answer(response_title, reply_markup=ReplyKeyboardRemove())
    await message.answer(response_body, reply_markup=start())


# обработка ответа откуда и куда
@router.message()
async def set_start_point(message: Message):
    if not data_for_send_req['toggle']:
        print(f'message.text-start - {message.text}')
        data_for_send_req['start_point'] = 's9601796'
        data_for_send_req['toggle'] = True
        await message.answer(str(data_for_send_req), reply_markup=chose_start_end())
    else:
        print(f'message.text-finish - {message.text}')
        data_for_send_req['end_point'] = 'c33897'
        data_for_send_req['toggle'] = False
        await message.answer(str(data_for_send_req), reply_markup=chose_finish())
