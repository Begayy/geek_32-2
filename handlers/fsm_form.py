from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes
from config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup


class FormStates(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    photo = State()


async def fsm_start(message: types.Message):
    await message.reply("Отправьте свой новый никнейм")
    await FormStates.nickname.set()


async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text

    await FormStates.next()
    await message.reply("Отправьте свой возраст, используйте только числа")


async def load_age(message: types.Message,
                   state: FSMContext):
    try:
        if type(int(message.text)) != int:
            await message.reply("Отправляйте числа, "
                                "пожалуйста запустите регистрацию заново")
            await state.finish()
        else:
            async with state.proxy() as data:
                data['age'] = message.text
                await FormStates.next()
                await message.reply("Отправь мне свое фото(не в разрешении файла)")

    except ValueError as e:
        await state.finish()
        print(f"FSMAGE: {e}")
        await message.reply("Ошибка, отправляйте числа, "
                            "пожалуйста запустите регистрацию сначала")


async def load_photo(message: types.Message,
                     state: FSMContext):
    print(message.photo)
    path = await message.photo[-1].download(
        destination_dir=r"C:\Users\99655\PycharmProjects\geek_32_2\media"
    )
    async with state.proxy() as data:
        with open(path.name, 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f"*Nickname: *  {data['nickname']}\n"
                        f"*Age: * {data['age']}",
                parse_mode=types.ParseMode.MARKDOWN
            )


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["signup"])
    dp.register_message_handler(load_nickname,
                                state=FormStates.nickname,
                                content_types=['text'])
    dp.register_message_handler(load_age,
                                state=FormStates.age,
                                content_types=['text'])
    dp.register_message_handler(load_photo,
                                state=FormStates.photo,
                                content_types=ContentTypes.PHOTO)
