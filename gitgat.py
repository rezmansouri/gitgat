from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
import helpers

# Access Token of your bot acquired from @BotFather
token = ''


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi I\'m GitGat!\nI can send a subdirectory from a GitHub repository directly to you as zip! try /get along with the URL!")


def error(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='I\'m sorry something unexpected happened')


def get(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='You should provide a URL along with the command. like this:')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='/get https://github.com/rezmansouri/gitgat')
        return
    url = context.args[0]
    url, dir_name = helpers.validate_url(url)
    if dir_name is False:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Please give me a valid GitHub directory/repository URL\nfor example: https://github.com/rezmansouri/gitgat\nor: https://github.com/rust-lang/rust/tree/master/src/test')
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hold on I\'m fetching the files...')
    helpers.crawl(url, dir_name)
    helpers.make_archive(base_name=helpers.storage_address + dir_name, format='zip',
                         root_dir=helpers.storage_address + dir_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text='I fetched the files! I\'m sending them...')
    with open(f'{helpers.storage_address}/{dir_name}.zip', 'rb') as output:
        context.bot.send_document(chat_id=update.effective_chat.id, document=output,
                                  reply_to_message_id=update.effective_message.message_id)
    helpers.clear_storage(dir_name)


def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    get_handler = CommandHandler('get', get)
    dispatcher.add_handler(get_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()


if __name__ == '__main__':
    main()
