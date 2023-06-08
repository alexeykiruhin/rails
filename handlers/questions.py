from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.start_question import start
from keyboards.chose_date import chose_date
from keyboards.chose_start_end import chose_start_end, chose_finish, chose_hard_from, chose_hard_to, chose_station
from datetime import date, datetime

from handlers.func.func import get_code
from settings import API_KEY

router = Router()  # [1]


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
    'toggle': 0
}


# вспомогательные функции

def callback():
    print('CALLBACK')


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
            # print('response')
            data = await response.json()
            # print(data)
            return data


# def get_ecp_code(station_name):
# def get_ecp_code(station_name):
#
#     print(os.getcwd())
#     return 'parse'


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
    # print(data_for_send_req)
    data_for_send_req['toggle'] = 0
    await message.answer(
        f"Введите точку отправления:",
        reply_markup=chose_hard_from()
    )


@router.message(Text(text="куда", ignore_case=True))
async def answer_to(message: Message):
    # print(data_for_send_req)
    data_for_send_req['toggle'] = 1
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
    # print(data)
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
    # print(f'out - {out}')
    response_body = f'Время  Название электрички \n'
    for o in out:
        response_body = response_body + o + '\n'
    await message.answer(response_title, reply_markup=ReplyKeyboardRemove())
    await message.answer(response_body, reply_markup=start())


# обработка ответа откуда и куда
# @router.message()
# async def set_start_point(message: Message):
#     out_str: list = []
#     code = await get_code(message.text)
#     if not data_for_send_req['toggle']:
#         if len(code) == 1:
#             print('code = 1')
#             data_for_send_req['start_point'] = code[0][0]
#             data_for_send_req['toggle'] = True
#             await message.answer(str(data_for_send_req), reply_markup=chose_start_end())
#         else:
#             print(f'code - {code}')
#             for c in code:
#                 print(f'c - {c}')
#                 out_str.append(c[1])
#             print(out_str)
#             await message.answer(str(data_for_send_req), reply_markup=chose_station(out_str))
#     else:
#         # code = await get_code(message.text)
#         # out_str: str = ''
#         if len(code) == 1:
#             print('code = 1')
#             data_for_send_req['end_point'] = code[0][0]
#             data_for_send_req['toggle'] = False
#             await message.answer(str(data_for_send_req), reply_markup=chose_finish())
#         else:
#             print(f'code - {code}')
#             for c in code:
#                 print(f'c - {c[1]}')
#                 out_str.append(c[1])
#             print(f'out_str - {out_str}')
#             await message.answer(f"Найденных станций: {len(code)} \nВыберите нужную:", reply_markup=chose_station(out_str))

@router.message()
async def set_start_point(message: Message):
    out_str: list = []
    if data_for_send_req['toggle'] == 0:
        code = await get_code(message.text)
    else:
        code = await get_code(message.text)
    print(data_for_send_req['toggle'])
    if len(code) == 1:
        # 0 = точка отправления
        if data_for_send_req['toggle'] == 0:
            data_for_send_req['start_point'] = code[0][0]
            await message.answer(str(data_for_send_req), reply_markup=chose_start_end())
        # 1 = точка прибытия
        elif data_for_send_req['toggle'] == 1:
            data_for_send_req['end_point'] = code[0][0]
            await message.answer(str(data_for_send_req), reply_markup=chose_finish())
        # 2 = построить маршрут
        elif data_for_send_req['toggle'] == 2:
            pass
    else:
        for c in code:
            out_str.append(c[1])# тут надо передавать еще и айди и потом прокидыать его  в пункт 1
        await message.answer(str(data_for_send_req), reply_markup=chose_station(out_str))
