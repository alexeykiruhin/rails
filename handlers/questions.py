from aiogram import Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove

# from keyboards.date_picker import date_picker
from keyboards.start_question import start
from keyboards.chose_date import chose_date
from keyboards.chose_start_end import chose_start_end, chose_finish, chose_station
from datetime import date, datetime
from aiogram.types import CallbackQuery

from handlers.func.func import get_code
from settings import API_KEY

router = Router()  # [1]
data_for_send_req = {
    'transport_type': '',
    'start_point': '',
    'end_point': '',
    'current_date_str': '',
    'toggle': 0,
    'toggle_code': ''
}


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    data_for_send_req['transport_type'] = ''
    data_for_send_req['start_point'] = ''
    data_for_send_req['end_point'] = ''
    data_for_send_req['current_date_str'] = ''
    data_for_send_req['toggle'] = 0
    data_for_send_req['toggle_code'] = ''
    await message.answer(
        "Выберите транспорт:",
        reply_markup=start()
    )


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
        f"{str(data_for_send_req)}"
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
        f"{str(data_for_send_req)}"
        f"Введите точку отправления:",
        # reply_markup=chose_hard_from()
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Text(text="куда", ignore_case=True))
async def answer_to(message: Message):
    # print(data_for_send_req)
    data_for_send_req['toggle'] = 1
    await message.answer(
        f"Введите точку прибытия:",
        # reply_markup=chose_hard_to()
        reply_markup=ReplyKeyboardRemove()
    )


# обработка кнопки назад в финальном слайде
@router.message(Text(text="назад", ignore_case=True))
async def back(message: Message):
    await message.answer("Сегодня. Выберите место отправление и место прибытия:", reply_markup=chose_start_end())


# обработка финального слайда - поиск
@router.message(Text(text="поиск", ignore_case=True))
async def set_search(message: Message):
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
    data_for_send_req['transport_type'] = ''
    data_for_send_req['start_point'] = ''
    data_for_send_req['end_point'] = ''
    data_for_send_req['current_date_str'] = ''
    data_for_send_req['toggle'] = 0
    data_for_send_req['toggle_code'] = ''


@router.callback_query()
async def callback_handler(callback_query: CallbackQuery):
    data = callback_query.data
    print(f'data - {data}')
    print(f'callback_query - {callback_query}')
    if data_for_send_req['toggle'] == 0:
        data_for_send_req['start_point'] = data
        await callback_query.answer('Станция отправления выбрана')
        await callback_query.message.answer(str(data_for_send_req), reply_markup=chose_start_end())
    else:
        data_for_send_req['end_point'] = data
        await callback_query.answer('Станция прибытия выбрана')
        await callback_query.message.answer(str(data_for_send_req), reply_markup=chose_finish())
    # await callback_query.answer(data)

    # await bot.send_message(chat_id=callback_query.from_user.id,
    #                                   text="Please choose a finish point:",
    #                                   reply_markup=chose_finish())


@router.message(Text(text="Другая дата", ignore_case=True))
async def set_another_date_point(message: Message):
    print(f'message.text - {message.text}')
    await message.answer(
        f"Выбирете дату:",
        reply_markup=chose_finish()  # test
    )


@router.message()
async def set_start_point(message: Message):
    print(f'message - {message}')
    out_str: list = []

    # prev_toggle = 0
    if data_for_send_req['toggle'] == 2:
        # code = await get_code(message.text)
        print(f'toggle = 2__________________ : {message.text}')

        code = data_for_send_req['toggle_code']

    else:
        print('-------')
        code = await get_code(message.text)
    print(data_for_send_req['toggle'])
    print('code', code)
    if len(code) == 1:
        # 0 = точка отправления
        if data_for_send_req['toggle'] == 0:
            data_for_send_req['start_point'] = code[0][0]
            print(f'set start_point')
            await message.answer('set start_point', reply_markup=chose_start_end())
        # 1 = точка прибытия
        elif data_for_send_req['toggle'] == 1:
            data_for_send_req['end_point'] = code[0][0]
            print(f'set end_point')
            await message.answer('set end_point', reply_markup=chose_finish())
        # 2 = построить маршрут
        # elif data_for_send_req['toggle'] == 2:
        #     pass
    elif len(code) == 0:
        # пишем не найдена станция
        await message.answer(str(data_for_send_req), reply_markup=chose_station(out_str))
    else:
        for c in code:
            out_str.append([c[0], c[1]])  # тут надо передавать еще и айди и потом прокидыать его  в пункт 1
        # prev_toggle = data_for_send_req['toggle']
        # data_for_send_req['toggle'] = 2
        await message.answer(str(data_for_send_req), reply_markup=chose_station(out_str))
