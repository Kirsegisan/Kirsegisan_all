from telegram import Update, ReplyKeyboardMarkup, replykeyboardremove
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from teg_bot.key import TOKEN
from teg_bot.connect_to_database import stickers, inserd_sticker


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

    dispatcher.add_handler(bye_handler)
    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(hello_keybord)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    print('successful launch')
    updater.idle()


def faund_stikers(text):
    for stiker in stickers:
        if stiker in text.lower():
            return stickers[stiker]


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
    update.message.reply_sticker(faund_stikers(text))


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


def inserd_sticker(update: Update, context: CallbackContext):
    pass



if __name__ == '__main__':
    main()
