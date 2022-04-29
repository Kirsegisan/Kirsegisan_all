from telegram import Update, ReplyKeyboardMarkup, replykeyboardremove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, ConversationHandler
from teg_bot.key import TOKEN
from teg_bot.connect_to_database import stickers, inserd_sticker


WAIT_NAME, WAIT_SEX, WAIT_GRADE = range(3)


def main():

    updater = Updater(
        token=TOKEN,
        use_context=True
    )
    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.all, echo)

    hello_keybord = MessageHandler(Filters.text('keybord'), keybord)

    hello_handler = MessageHandler(Filters.text('Hello, hello'), say_hello)

    bye_handler = MessageHandler(Filters.text('Goodbye, goodbye'), say_bye)

    meet_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text("Привет"), meet)],
        states={
            WAIT_NAME: [MessageHandler(Filters.text, ask_sex)],
            WAIT_SEX: [MessageHandler(Filters.text, ask_grade)],
            WAIT_GRADE: [MessageHandler(Filters.text, greet)]
        }
    )

    dispatcher.add_handler(bye_handler)
    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(hello_keybord)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print('successful launch')
    updater.idle()





def found_stickers(text):
    for sticker in stickers:
        if sticker in text.lower():
            return stickers[sticker]


def echo(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name
    update.message.reply_text(f"Hello, {name}. Yours message {text}\n"
                              f'Yours id {chat_id}')


def say_hello(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    update.message.reply_text(f"Hello, {name}. I'm bot, friend")


def say_bye(update: Update, context: CallbackContext):
    name = update.message.from_user.first_name
    text = update.message.text
    update.message.reply_text(f"Goodbye, {name}.")
    update.message.reply_sticker(found_stickers(text))


def keybord(update: Update, context: CallbackContext):
    buttons = [
        ['1', '2', 'new sticker'],
        ['hello', 'goodbye']
    ]
    update.message.reply_text(
        text='Now, you have kaybords',
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True
        )

    )


def new_sticker(update: Update, context: CallbackContext):
    sticker_id = update.message.sticker.file_id
    for keyword in stickers:
        if sticker_id == stickers[keyword]:
            update.message.reply_text('I have this to')
            update.message.reply_stickers(sticker_id)
            break
    else:
        context.user_data['new_sticker'] = sticker_id
        update.message.reply_text("I haven't this")


def new_keyword(update: Update, context: CallbackContext):
    if 'new_sticker' not in context.user_data:
        say_bye(update, context)
    else:
        keyword = update.message.text
        sticker_id = context.user_data['new_sticker']
        inserd_sticker(keyword, sticker_id)
        context.user_data.clear()


def meet(update: Update, context: CallbackContext):
    """
    имя
    пол
    класс
    id юзера

    """
    user_id = update.message.from_user.id
    if in_database(user_id):
        pass  # выход из диолога
    ask_name(update, context)


def ask_name(update: Update, context: CallbackContext):
    """
    имя?
    TODO проверить имя пользователя в телеге
    """
    update.message.reply_text(
        "Вас нет в базе\n"
        "Войдите в базу!\n"
        "Введите свое имя"
    )
    return WAIT_NAME


def ask_sex(update: Update, context: CallbackContext):
    """
    пол?
    """
    name = update.message.text
    if not name_is_vaklid(name):
        update.message.reply_text(
            "Вас нет в базе\n"
            "Войдите в базу!\n"
            "Введите свое имя"
        )
        return WAIT_NAME
    context.user_data["name"] = name
    buttons = [
        ["М", "Ж"]
    ]
    keys = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
    reply_text = f"Введите свой пол"
    update.message.reply_text(
        reply_text,
        reply_markup=keys
    )


def ask_grade(update: Update, context: CallbackContext):
    """
    класс?
    """
    sex = update.message.text
    context.user_data["sex"] = sex
    buttons = [
        ["1-8", "9-11"]
    ]
    keys = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
    reply_text = f"Введите свой класс"
    update.message.reply_text(
        reply_text,
        reply_markup=keys
    )


def greet(update: Update, context: CallbackContext):
    """
    записывает в БД
        user_id(сообщение)
        name(контекст)
        sex((контекст)
        grade(из пред. сооб.)
    """
    grade = update.message.text
    name = context.user_data["name"]
    sex = context.user_data["sex"]
    user_id = update.message.from_user.id

    insert_user(user_id, name, sex, grade)
    update.message.reply_text(
        f'Новая запись в БД\n'
        f'{user_id=}\n'
        f'{name=}\n'
        f'{sex=}\n'
        f'{grade=}\n'
    )


def name_is_vaklid(name: str) -> bool:
    return name.isalpha()


def sex_is_vaklid(sex: str) -> bool:
    return True
    

def grade_is_vaklid(grade: str) -> bool:
    return True

            
if __name__ == '__main__':
    main()
