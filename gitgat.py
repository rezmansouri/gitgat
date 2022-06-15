from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
from uuid import uuid1
import logging
import helpers

# Access Token of your bot acquired from @BotFather
token = ''


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi I\'m GitGat!\nI can send a subdirectory from a GitHub repository directly to you as zip! try /get along with the URL!")


def error(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='I\'m sorry something unexpected happened')
    print(context.error)


def get(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='You should provide a URL along with the command. like this:')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/get https://github.com/rezmansouri/gitgat')
        return
    url = context.args[0]
    url, file_name = helpers.validate_url(url)
    if file_name is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Please give me a valid GitHub directory/repository URL\nfor example: https://github.com/rezmansouri/gitgat\nor: https://github.com/rust-lang/rust/tree/master/src/test')
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hold on I\'m fetching the files...')
    unique_dir = str(uuid1())
    helpers.crawl(url, unique_dir)
    helpers.make_archive(base_name=helpers.storage_address + unique_dir, format='zip',
                         root_dir=helpers.storage_address + unique_dir)
    context.bot.send_message(chat_id=update.effective_chat.id, text='I fetched the files! I\'m sending them...')
    with open(f'{helpers.storage_address}/{unique_dir}.zip', 'rb') as output:
        context.bot.send_document(chat_id=update.effective_chat.id, document=output,
                                  reply_to_message_id=update.effective_message.message_id, filename=file_name)
    helpers.clear_storage(unique_dir)


def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    get_handler = CommandHandler('get', get)
    dispatcher.add_handler(get_handler)

    dispatcher.add_error_handler(error)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    updater.start_polling()


if __name__ == '__main__':
    main()
