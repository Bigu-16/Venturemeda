from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler,filters,CallbackContext

users_contact_shared = set()

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if user_id in users_contact_shared:
        await update.message.reply_text('Welcome back!', reply_markup=ReplyKeyboardRemove())
        

    else:
        await context.bot.send_photo(
            chat_id = chat_id,
            photo = "C:/Users/abget/Downloads/welcome.jpg",
            caption = "Hello, welcome to Venturemeda! "
        )

        # Create "Share My Contact" button
        contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]

        reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

        # Send the new button
        await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)


    # users_contact_shared.discard(user_id)

    


    # Function to handle contact sharing
async def contact_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    contact = update.message.contact

    user_id = user.id

    if contact:
        phone_number = contact.phone_number
        username = user.username if user.username else "No username"

        users_contact_shared.add(user_id)
        
        # Send user contact details
        await update.message.reply_text(f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
        reply_markup=ReplyKeyboardRemove()                                
        )

async def block_messages(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in users_contact_shared:
        await update.message.reply_text("You must share your contact first please press the share my contact button.")
        return 
    
def main():
    app = Application.builder().token('7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE').build()
    
    app.add_handler(CommandHandler('start',start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))

    app.run_polling()

if __name__ == '__main__':
    main()