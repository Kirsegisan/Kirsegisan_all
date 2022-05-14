from telegram import Update, ReplyKeyboardMarkup, replykeyboardremove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, ConversationHandler
from teleg_bot.key import TOKEN
from teleg_bot.connect_to_database import stickers, inserd_sticker, in_database, inserd_user


WAIT_NAME, WAIT_SEX, WAIT_GRADE = range(3)
buttons_grade = [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", '10', '11' ]
    ]

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

    stickers_hendler = MessageHandler(Filters.sticker, new_sticker)

    keyword_hendler = MessageHandler(Filters.text, new_keyword)

    meet_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('Hello, hello'), meet)],
        states={
            WAIT_NAME: [MessageHandler(Filters.text, ask_sex)],
            WAIT_SEX: [MessageHandler(Filters.text, ask_grade)],
            WAIT_GRADE: [MessageHandler(Filters.text, greet)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(meet_handler)
    dispatcher.add_handler(stickers_hendler)
    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(bye_handler)
    dispatcher.add_handler(hello_keybord)
    dispatcher.add_handler(keyword_hendler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print('successful launch')
    updater.idle()





#def found_stickers(text):
#    for sticker in stickers:
#        if sticker in text.lower():
#            return stickers[sticker]


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


def keybord(update: Update, context: CallbackContext):
    buttons = [
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
    sticker_unique_id = update.message.sticker.file_unique_id
    for stickers_unique_id in stickers:
        if sticker_unique_id == stickers[stickers_unique_id]:
            update.message.reply_text('I have this to')
            update.message.reply_sticker(sticker_id)
            break

    else:
        context.user_data['new_sticker'] = sticker_unique_id
        update.message.reply_text("I haven't this\n"
                                  'give me the kyeword for this sticker')


def new_keyword(update: Update, context: CallbackContext):
    if 'new_sticker' not in context.user_data:
        echo(update, context)
    else:
        keyword = update.message.text
        sticker_id = context.user_data['new_sticker']
        inserd_sticker(keyword, sticker_id)
        context.user_data.clear()
        update.message.reply_text('thanks')


def meet(update: Update, context: CallbackContext):
    """
    Name
    sex
    Grade
    id user

    """
    user_id = update.message.from_user.id
    if in_database(user_id):
        update.message.reply_text(
            'welcome back'
            #reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    return ask_name(update, context)


def ask_name(update: Update, context: CallbackContext):
    """
    имя?
    TODO проверить имя пользователя в телеге
    """
    update.message.reply_text(
        "Who are you?\n"
        "you're not in database!\n"
        "What's your name?"
    )
    return WAIT_NAME


def ask_sex(update: Update, context: CallbackContext):
    """
    пол?
    """
    name = update.message.text
    if not name_is_vaklid(name):
        update.message.reply_text(
            "Who are you?\n"
            "you're not in db!\n"
            "What's your name?\n"
            "!!!name has onle letters!!!"
        )
        return WAIT_NAME
    context.user_data["name"] = name
    buttons_sex = [
        ["M", "W"]
    ]
    keys = ReplyKeyboardMarkup(
        buttons_sex,
        resize_keyboard=True
    )
    reply_text = f"What gender are you?"
    update.message.reply_text(
        reply_text,
        reply_markup=keys
    )
    return WAIT_SEX


def ask_grade(update: Update, context: CallbackContext):
    """
    класс?
    """
    sex = update.message.text
    if not sex_is_vaklid(sex):
        update.message.reply_text(
            "What gender are you?\n"
            '!!! M or W!!!'
        )
        return WAIT_SEX

    context.user_data["sex"] = sex
    keys = ReplyKeyboardMarkup(
        buttons_grade,
        resize_keyboard=True
    )
    reply_text = f"What grade are you in?"
    update.message.reply_text(
        reply_text,
        reply_markup=keys
    )
    return WAIT_GRADE


def greet(update: Update, context: CallbackContext):
    """
    записывает в БД
        user_id(сообщение)
        name(контекст)
        sex((контекст)
        grade(из пред. сооб.)
    """
    grade = update.message.text
    if not grade_is_vaklid(grade):
        update.message.reply_text(
            '!!! it not really !!!\n'
            "What grade are you in?"
        )
        return WAIT_GRADE
    name = context.user_data["name"]
    sex = context.user_data["sex"]
    user_id = update.message.from_user.id

    inserd_user(user_id, name, sex, grade)

    update.message.reply_text(
        f"now you're in database\n"
        f'{user_id=}\n'
        f'{name=}\n'
        f'{sex=}\n'
        f'{grade=}\n'
    )
    return ConversationHandler.END


def name_is_vaklid(name: str) -> bool:
    return name.isalpha()


def sex_is_vaklid(sex: str) -> bool:
    return sex == 'M' or sex == "W"
    

def grade_is_vaklid(grade: str) -> bool:
    return grade in ["1", "2", "3", "4", "5", "6", "7", "8", "9", '10', '11' ]

            
if __name__ == '__main__':
    main()
