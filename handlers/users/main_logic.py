from loader import dp
from aiogram import types
import requests
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from keyboards.inline.change_menu import markup_start, markup_middle, markup_end


async def get_data(country_name):
    # updating date information
    current_data = datetime.today().strftime('%d.%m.%Y')
    month_ago = (datetime.today() - timedelta(days=31)).strftime('%d.%m.%Y')

    the_name = country_name.lower()

    url = "https://vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com/api/npm-covid-data/"

    headers = {
        "X-RapidAPI-Key": "2d21880ffcmsh4af669a56379968p14ec84jsn4b232373db9e",
        "X-RapidAPI-Host": "vaccovid-coronavirus-vaccine-and-treatment-tracker.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers).json()

    information_list = list()
    for country in response:
        if the_name in country['Country'].lower() or \
                the_name in country['Continent'].lower():
            # don't change key names, this is how API works

            msg = f"Current data: {current_data}\n" \
                  f"<i>Information is current for the last month</i>: {month_ago}\n\n" \
                  f"Country name: {country['Country']}\n" \
                  f"Continent: {country['Continent']}\n" \
                  f"Infection risk: {country['Infection_Risk']}\n" \
                  f"Case fatality rate: {country['Case_Fatality_Rate']}\n" \
                  f"Recovery proportion: {country['Recovery_Proporation']}\n\n" \
                  f"<b>NEW DATA</b>\n" \
                  f"Cases: {country['NewCases']}\n" \
                  f"Deaths: {country['NewDeaths']}\n" \
                  f"New recovered: {country['NewRecovered']}\n\n" \
                  f"<b>TOTAL DATA</b>\n" \
                  f"Cases: {country['TotalCases']}\n" \
                  f"Deaths: {country['TotalDeaths']}\n" \
                  f"Total recovered: {country['TotalRecovered']}\n\n" \
                  f"Active cases: {country['ActiveCases']}"
            information_list.append(msg)
    return information_list


@dp.message_handler()
async def give_info(message: types.Message, state: FSMContext):

    information_list = await get_data(message.text)
    length = len(information_list)
    page_index = 0

    page_info = f"\n\npage: {page_index + 1}/{length}"
    if information_list:
        if length == 1:
            await message.answer(information_list[page_index])
        else:
            await message.answer(
                information_list[page_index] + page_info,
                reply_markup=markup_start
            )
    else:
        await message.reply('Incorrect name')

    # setting data
    await state.set_data(
        {
            'information_list': information_list,
            'length': length,
            'page_index': page_index
        }
    )


@dp.callback_query_handler(text='next')
async def next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    information_list = data['information_list']
    length = data['length']
    page_index = data['page_index']

    page_info = f"\n\npage: {page_index + 2}/{length}"
    if page_index == length - 2:
        await call.message.edit_text(
            text=information_list[page_index+1] + page_info,
            reply_markup=markup_end
        )
    else:
        await call.message.edit_text(
            text=information_list[page_index+1] + page_info,
            reply_markup=markup_middle
        )

    await state.update_data(
        {
            'page_index': page_index + 1
        }
    )


@dp.callback_query_handler(text='back')
async def next_page(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    information_list = data['information_list']
    length = data['length']
    page_index = data['page_index']

    page_info = f"\n\npage: {page_index}/{length}"
    if page_index - 1 == 0:
        await call.message.edit_text(
            text=information_list[page_index] + page_info,
            reply_markup=markup_start
        )
    else:
        await call.message.edit_text(
            text=information_list[page_index] + page_info,
            reply_markup=markup_middle
        )

    await state.update_data(
        {
            'page_index': page_index - 1
        }
    )
