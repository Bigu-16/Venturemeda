# from telegram.ext import Application,CommandHandler, MessageHandler, filters

# async def start(update,context):
#     await update.message.reply_text('Welcom to Venturemeda_bot, Would you like to share your contact?')

# async def echo(update,context):
#     await update.message.reply_text(f"You said: {update.message.text}")

# application = Application.builder().token('7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE').build()

# application.add_handler(CommandHandler('start',start))
# application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
# application.run_polling()

# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from telegram.ext import Application, CommandHandler, MessageHandler,filters,CallbackContext

# users_contact_shared = set()

# async def start(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user_id = update.message.from_user.id

#     if user_id in users_contact_shared:
#         await update.message.reply_text('Welcome back!', reply_markup=ReplyKeyboardRemove())
        

#     else:
#         await context.bot.send_photo(
#             chat_id = chat_id,
#             photo = "C:/Users/abget/Downloads/welcome.jpg",
#             caption = "Hello, welcome to Venturemeda! "
#         )

#         # Create "Share My Contact" button
#         contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]

#         reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

#         # Send the new button
#         await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)


#     # users_contact_shared.discard(user_id)

    


#     # Function to handle contact sharing
# async def contact_handler(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     contact = update.message.contact

#     user_id = user.id

#     if contact:
#         phone_number = contact.phone_number
#         username = user.username if user.username else "No username"

#         users_contact_shared.add(user_id)
        
#         # Send user contact details
#         await update.message.reply_text(f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
#         reply_markup=ReplyKeyboardRemove()                                
#         )

# async def block_messages(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id not in users_contact_shared:
#         await update.message.reply_text("You must share your contact first please press the share my contact button.")
#         return 
    
# def main():
#     app = Application.builder().token('7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE').build()
    
#     app.add_handler(CommandHandler('start',start))
#     app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
#     app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))

#     app.run_polling()

# if __name__ == '__main__':
#     main()



# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# users_contact_shared = set()
# user_courses = {}  # Dictionary to store enrolled courses per user

# # Sample courses (Dictionary format: Course Name -> List of Materials)
# COURSES = {
#     "Python Basics": ["https://example.com/python_video.mp4", "https://example.com/python_notes.pdf"],
#     "Web Development": ["https://example.com/web_video.mp4", "https://example.com/web_notes.pdf"]
# }

# # Define states for conversation
# SELECT_COURSE = 1

# async def start(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user_id = update.message.from_user.id

#     if user_id in users_contact_shared:
#         # Show Explore Courses and My Courses buttons
#         menu_buttons = [
#             [KeyboardButton("📚 Explore Courses"), KeyboardButton("📂 My Courses")]
#         ]
#         reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=True)
#         await update.message.reply_text('Welcome back! Choose an option:', reply_markup=reply_markup)
#     else:
#         await context.bot.send_photo(
#             chat_id=chat_id,
#             photo="C:/Users/abget/Downloads/welcome.jpg",
#             caption="Hello, welcome to Venturemeda!"
#         )

#         contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
#         reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)
#         await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)

# async def contact_handler(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     contact = update.message.contact
#     user_id = user.id

#     if contact:
#         phone_number = contact.phone_number
#         username = user.username if user.username else "No username"

#         users_contact_shared.add(user_id)
#         user_courses[user_id] = []  # Initialize an empty course list for the user

#         menu_buttons = [
#             [KeyboardButton("📚 Explore Courses"), KeyboardButton("📂 My Courses")]
#         ]
#         reply_markup = ReplyKeyboardMarkup(menu_buttons, resize_keyboard=True, one_time_keyboard=True)

#         await update.message.reply_text(
#             f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
#             reply_markup=reply_markup
#         )

# async def block_messages(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id not in users_contact_shared:
#         await update.message.reply_text("You must share your contact first. Please press the 'Share My Contact' button.")
#         return 

# # Show all available courses
# async def explore_courses(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

#     await update.message.reply_text("📚 Select a course to enroll:", reply_markup=reply_markup)
#     return SELECT_COURSE

# # Enroll user in a selected course
# async def enroll_in_course(update: Update, context: CallbackContext) -> int:
#     user_id = update.message.from_user.id
#     course_name = update.message.text

#     if course_name in COURSES:
#         if course_name not in user_courses[user_id]:
#             user_courses[user_id].append(course_name)
#             await update.message.reply_text(f"✅ You have enrolled in *{course_name}*!", parse_mode="Markdown")
#         else:
#             await update.message.reply_text("⚠️ You are already enrolled in this course.")

#     return ConversationHandler.END

# # Show courses the user has enrolled in
# async def my_courses(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     enrolled_courses = user_courses.get(user_id, [])

#     if enrolled_courses:
#         response = "📂 *Your Enrolled Courses:*\n\n"
#         response += "\n".join([f"✅ {course}" for course in enrolled_courses])
#     else:
#         response = "❌ You have not enrolled in any courses yet."

#     await update.message.reply_text(response, parse_mode="Markdown")

# def main():
#     app = Application.builder().token('YOUR_BOT_TOKEN').build()
    
#     app.add_handler(CommandHandler('start', start))
#     app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
#     app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))
#     app.add_handler(MessageHandler(filters.Regex("^📚 Explore Courses$"), explore_courses))
#     app.add_handler(MessageHandler(filters.Regex("^📂 My Courses$"), my_courses))

#     # Add conversation handler for selecting a course
#     course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, explore_courses)],
#         states={SELECT_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_in_course)]},
#         fallbacks=[]
#     )
    
#     app.add_handler(course_handler)

#     app.run_polling()

# if __name__ == '__main__':
#     main()

# No back button , asks course title twice
# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputFile
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
# import json

# ADMIN_ID = 314589754  # Replace with your Telegram user ID

# # Storage for courses
# COURSES = {}

# # Load & Save Functions for Persistence
# def save_courses():
#     with open("courses.json", "w") as file:
#         json.dump(COURSES, file)

# def load_courses():
#     global COURSES
#     try:
#         with open("courses.json", "r") as file:
#             COURSES = json.load(file)
#     except FileNotFoundError:
#         COURSES = {}

# # Load courses on start
# load_courses()

# # Define states for conversation
# ADD_COURSE, DELETE_COURSE, UPLOAD_VIDEO, UPLOAD_PDF = range(4)

# async def start(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id

#     if user_id == ADMIN_ID:
#         admin_buttons = [
#             ["➕ Add Course", "🗑 Delete Course"],
#             ["📹 Upload Video", "📄 Upload PDF"],
#             ["📂 View Courses"]
#         ]
#         reply_markup = ReplyKeyboardMarkup(admin_buttons, resize_keyboard=True, one_time_keyboard=True)
#         await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=reply_markup)
#     else:
#         await update.message.reply_text("❌ You are not authorized to manage courses.")

# # ➕ Add Course
# async def add_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the new course name:")
#     return ADD_COURSE

# async def save_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text
#     if course_name in COURSES:
#         await update.message.reply_text("⚠️ Course already exists!")
#     else:
#         COURSES[course_name] = []
#         save_courses()
#         await update.message.reply_text(f"✅ Course '{course_name}' added!")
#     return ConversationHandler.END

# # 🗑 Delete Course
# async def delete_course(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
#     await update.message.reply_text("Select a course to delete:", reply_markup=reply_markup)
#     return DELETE_COURSE

# async def remove_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text
#     if course_name in COURSES:
#         del COURSES[course_name]
#         save_courses()
#         await update.message.reply_text(f"✅ Course '{course_name}' deleted!")
#     else:
#         await update.message.reply_text("⚠️ Course not found!")
#     return ConversationHandler.END

# # 📹 Upload Video
# async def upload_video(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
#     await update.message.reply_text("Select a course to add a video:", reply_markup=reply_markup)
#     return UPLOAD_VIDEO

# async def receive_video(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     user_data["selected_course"] = update.message.text

#     await update.message.reply_text("Send the video file now:")
#     return UPLOAD_VIDEO

# async def save_video(update: Update, context: CallbackContext) -> int:
#     video = update.message.video
#     selected_course = context.user_data.get("selected_course")

#     if selected_course and video:
#         file_id = video.file_id
#         COURSES[selected_course].append(f"Video: {file_id}")
#         save_courses()
#         await update.message.reply_text(f"✅ Video added to '{selected_course}'!")
#     else:
#         await update.message.reply_text("⚠️ Something went wrong.")
#     return ConversationHandler.END

# # 📄 Upload PDF
# async def upload_pdf(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
#     await update.message.reply_text("Select a course to add a PDF:", reply_markup=reply_markup)
#     return UPLOAD_PDF

# async def receive_pdf(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     user_data["selected_course"] = update.message.text

#     await update.message.reply_text("Send the PDF file now:")
#     return UPLOAD_PDF

# async def save_pdf(update: Update, context: CallbackContext) -> int:
#     document = update.message.document
#     selected_course = context.user_data.get("selected_course")

#     if selected_course and document:
#         file_id = document.file_id
#         COURSES[selected_course].append(f"PDF: {file_id}")
#         save_courses()
#         await update.message.reply_text(f"✅ PDF added to '{selected_course}'!")
#     else:
#         await update.message.reply_text("⚠️ Something went wrong.")
#     return ConversationHandler.END

# # 📂 View Courses
# async def view_courses(update: Update, context: CallbackContext) -> None:
#     if COURSES:
#         response = "📂 *Available Courses:*\n\n"
#         for course, materials in COURSES.items():
#             response += f"📌 {course}\n"
#             for item in materials:
#                 response += f"  - {item}\n"
#             response += "\n"
#     else:
#         response = "❌ No courses available."

#     await update.message.reply_text(response, parse_mode="Markdown")

# def main():
#     app = Application.builder().token('7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE').build()

#     app.add_handler(CommandHandler('start', start))

#     # Admin Commands
#     app.add_handler(MessageHandler(filters.Regex("^➕ Add Course$"), add_course))
#     app.add_handler(MessageHandler(filters.Regex("^🗑 Delete Course$"), delete_course))
#     app.add_handler(MessageHandler(filters.Regex("^📹 Upload Video$"), upload_video))
#     app.add_handler(MessageHandler(filters.Regex("^📄 Upload PDF$"), upload_pdf))
#     app.add_handler(MessageHandler(filters.Regex("^📂 View Courses$"), view_courses))

#     # Conversation Handlers
#     add_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, add_course)],
#         states={ADD_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
#         fallbacks=[]
#     )

#     delete_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, delete_course)],
#         states={DELETE_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_course)]},
#         fallbacks=[]
#     )

#     upload_video_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, upload_video)],
#         states={UPLOAD_VIDEO: [MessageHandler(filters.VIDEO, save_video)]},
#         fallbacks=[]
#     )

#     upload_pdf_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, upload_pdf)],
#         states={UPLOAD_PDF: [MessageHandler(filters.Document.PDF, save_pdf)]},
#         fallbacks=[]
#     )

#     app.add_handler(add_course_handler)
#     app.add_handler(delete_course_handler)
#     app.add_handler(upload_video_handler)
#     app.add_handler(upload_pdf_handler)

#     app.run_polling()

# if __name__ == '__main__':
#     main()


# the delete course is not working ...when it is pressed it is adding it to courses ...the same goes to upload video and file 

# when i press the upload video it is asking to select a course and when i do it says course already exists shouldn't it add the video to the course when i choose the course

# from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
# import json

# # 🔹 Allow multiple admins
# ADMIN_IDS = [314589754, 6635151682]  # Replace with actual admin Telegram IDs

# # 🔹 Storage for courses (will be stored in a JSON file)
# COURSES = {}

# # 🔹 Load & Save Functions
# def save_courses():
#     with open("courses.json", "w") as file:
#         json.dump(COURSES, file, indent=4)

# def load_courses():
#     global COURSES
#     try:
#         with open("courses.json", "r") as file:
#             COURSES = json.load(file)
#     except FileNotFoundError:
#         COURSES = {}

# # 🔹 Load courses on startup
# load_courses()

# # 🔹 Conversation states
# ADD_COURSE, UPLOAD_VIDEO, UPLOAD_PDF = range(3)

# async def start(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id

#     if user_id in ADMIN_IDS:
#         buttons = [
#             ["➕ Add Course", "🗑 Delete Course"],
#             ["📹 Upload Video", "📄 Upload PDF"],
#             ["📂 View Courses"]
#         ]
#         reply_markup = ReplyKeyboardMarkup(buttons + [["⬅ Back to Menu"]], resize_keyboard=True)
#         await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=reply_markup)
#     else:
#         await update.message.reply_text("❌ You are not authorized to manage courses.")

# # ➕ **Add Course**
# async def add_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text

#     if course_name in COURSES:
#         await update.message.reply_text("⚠️ Course already exists! Try again.")
#     else:
#         COURSES[course_name] = []
#         save_courses()
#         await update.message.reply_text(f"✅ Course '{course_name}' added!")

#     return ConversationHandler.END

# # 📹 **Upload Video**
# async def upload_video(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()] + [["⬅ Back to Menu"]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#     await update.message.reply_text("Select a course to add a video:", reply_markup=reply_markup)
#     return UPLOAD_VIDEO

# async def receive_video(update: Update, context: CallbackContext) -> int:
#     selected_course = update.message.text
#     context.user_data["selected_course"] = selected_course

#     if selected_course == "⬅ Back to Menu":
#         return await start(update, context)

#     await update.message.reply_text("Send the video file now:")
#     return UPLOAD_VIDEO

# async def save_video(update: Update, context: CallbackContext) -> int:
#     video = update.message.video
#     selected_course = context.user_data.get("selected_course")

#     if selected_course and video:
#         file_id = video.file_id
#         COURSES[selected_course].append(f"Video: {file_id}")
#         save_courses()
#         await update.message.reply_text(f"✅ Video added to '{selected_course}'!")

#     return ConversationHandler.END

# # 📄 **Upload PDF**
# async def upload_pdf(update: Update, context: CallbackContext) -> int:
#     keyboard = [[course] for course in COURSES.keys()] + [["⬅ Back to Menu"]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
#     await update.message.reply_text("Select a course to add a PDF:", reply_markup=reply_markup)
#     return UPLOAD_PDF

# async def receive_pdf(update: Update, context: CallbackContext) -> int:
#     selected_course = update.message.text
#     context.user_data["selected_course"] = selected_course

#     if selected_course == "⬅ Back to Menu":
#         return await start(update, context)

#     await update.message.reply_text("Send the PDF file now:")
#     return UPLOAD_PDF

# async def save_pdf(update: Update, context: CallbackContext) -> int:
#     document = update.message.document
#     selected_course = context.user_data.get("selected_course")

#     if selected_course and document:
#         file_id = document.file_id
#         COURSES[selected_course].append(f"PDF: {file_id}")
#         save_courses()
#         await update.message.reply_text(f"✅ PDF added to '{selected_course}'!")

#     return ConversationHandler.END

# # 📂 **View Courses**
# async def view_courses(update: Update, context: CallbackContext) -> None:
#     if COURSES:
#         response = "📂 *Available Courses:*\n\n"
#         for course, materials in COURSES.items():
#             response += f"📌 {course}\n"
#             for item in materials:
#                 response += f"  - {item}\n"
#             response += "\n"
#     else:
#         response = "❌ No courses available."

#     await update.message.reply_text(response, parse_mode="Markdown")

# # 🔹 **Handlers & Main Function**
# def main():
#     app = Application.builder().token('7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE').build()

#     app.add_handler(CommandHandler('start', start))

#     # Admin Handlers
#     app.add_handler(MessageHandler(filters.Regex("^➕ Add Course$"), add_course))
#     app.add_handler(MessageHandler(filters.Regex("^📹 Upload Video$"), upload_video))
#     app.add_handler(MessageHandler(filters.Regex("^📄 Upload PDF$"), upload_pdf))
#     app.add_handler(MessageHandler(filters.Regex("^📂 View Courses$"), view_courses))
    
#     # Back to menu handler
#     app.add_handler(MessageHandler(filters.Regex("^⬅ Back to Menu$"), start))

#     # Conversation Handlers
#     add_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, add_course)],
#         states={ADD_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course)]},
#         fallbacks=[]
#     )

#     upload_video_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, upload_video)],
#         states={UPLOAD_VIDEO: [MessageHandler(filters.VIDEO, save_video)]},
#         fallbacks=[]
#     )

#     upload_pdf_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, upload_pdf)],
#         states={UPLOAD_PDF: [MessageHandler(filters.Document.PDF, save_pdf)]},
#         fallbacks=[]
#     )

#     app.add_handler(add_course_handler)
#     app.add_handler(upload_video_handler)
#     app.add_handler(upload_pdf_handler)

#     app.run_polling()

# if __name__ == '__main__':
#     main()


# this works file for admin

# import sqlite3
# from telegram import (
#     Update, 
#     ReplyKeyboardMarkup, 
#     KeyboardButton, 
#     ReplyKeyboardRemove
# )
# from telegram.ext import (
#     Application, 
#     CommandHandler, 
#     MessageHandler, 
#     filters, 
#     CallbackContext, 
#     ConversationHandler
# )

# TOKEN = "7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE"
# DB_PATH = "courses.db"

# # Define user roles
# ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
# STUDENTS = set()

# # Conversation states
# ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE = range(4)

# # Database setup
# def setup_database():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS files (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         course_name TEXT,
#         file_type TEXT,
#         file_id TEXT,
#         FOREIGN KEY(course_name) REFERENCES courses(name)
#     )''')

#     conn.commit()
#     conn.close()

# setup_database()

# # Admin keyboard
# def admin_menu():
#     return ReplyKeyboardMarkup(
#         [
#             ["➕ Add Course", "🗑 Delete Course"],
#             ["📤 Upload Video or PDF"],
#             ["📂 View Courses", "⬅ Back to Menu"]
#         ],
#         resize_keyboard=True
#     )

# # Student keyboard  
# def student_menu():
#     return ReplyKeyboardMarkup(
#         [["📖 Explore Courses", "📚 My Courses"]],
#         resize_keyboard=True
#     )

# async def start(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id

#     if user_id in ADMINS:
#         await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
#     else:
#         STUDENTS.add(user_id)
#         await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())

# # ➕ Add Course Flow
# async def add_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
#     return ADDING_COURSE

# async def save_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     try:
#         cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
#         conn.commit()
#         await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
#     except sqlite3.IntegrityError:
#         await update.message.reply_text("⚠ Course already exists.")

#     conn.close()
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 🗑 Delete Course Flow
# async def delete_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
#     return DELETING_COURSE

# async def confirm_delete(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📤 Upload Video or PDF Flow
# async def select_course(update: Update, context: CallbackContext) -> int:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ No courses available. Please add a course first.")
#         return ConversationHandler.END

#     course_buttons = [[course] for course in courses]
#     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

#     await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
#     return SELECTING_COURSE

# async def upload_file(update: Update, context: CallbackContext) -> int:
#     context.user_data["selected_course"] = update.message.text.strip()
#     await update.message.reply_text("📤 Send the video or PDF file:")
#     return UPLOADING_FILE

# async def save_file(update: Update, context: CallbackContext) -> int:
#     file = update.message.video or update.message.document
#     file_id = file.file_id
#     file_type = "video" if update.message.video else "pdf"
#     course_name = context.user_data["selected_course"]

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📂 View Courses
# async def view_courses(update: Update, context: CallbackContext) -> None:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]

#     if not courses:
#         await update.message.reply_text("⚠ No courses available.")
#     else:
#         message = "📂 Available Courses:\n"
#         for course in courses:
#             message += f"\n📌 {course}\n"
#             cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
#             files = cursor.fetchall()
#             for file_type, file_id in files:
#                 file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
#                 message += f"  - {file_type_display}: {file_id}\n"

#     conn.close()
#     await update.message.reply_text(message)

# # ⬅ Back to Menu
# async def back_to_menu(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id in ADMINS:
#         await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
#     else:
#         await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

# def main():
#     app = Application.builder().token(TOKEN).build()

#     add_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
#         states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
#         fallbacks=[]
#     )

#     delete_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
#         states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
#         fallbacks=[]
#     )

#     upload_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("📹 Upload Video|📄 Upload PDF"), select_course)],
#         states={
#             SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
#             UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
#         },
#         fallbacks=[]
#     )

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(add_course_handler)
#     app.add_handler(delete_course_handler)
#     app.add_handler(upload_handler)
#     app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
#     app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))

#     app.run_polling()

# if __name__ == "__main__":
#     main()


# # import sqlite3
# # from telegram import (
# #     Update, 
# #     ReplyKeyboardMarkup, 
# #     KeyboardButton, 
# #     ReplyKeyboardRemove
# # )
# # from telegram.ext import (
# #     Application, 
# #     CommandHandler, 
# #     MessageHandler, 
# #     filters, 
# #     CallbackContext, 
# #     ConversationHandler
# # )

# # TOKEN = "7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE"
# # DB_PATH = "courses.db"

# # # Define user roles
# # ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
# # STUDENTS = set()

# # # Conversation states
# # ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE, ENROLLING_COURSE = range(5)

# # # Database setup
# # def setup_database():
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()

# #     cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         name TEXT UNIQUE
# #     )''')

# #     cursor.execute('''CREATE TABLE IF NOT EXISTS files (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         course_name TEXT,
# #         file_type TEXT,
# #         file_id TEXT,
# #         FOREIGN KEY(course_name) REFERENCES courses(name)
# #     )''')

# #     cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         student_id INTEGER,
# #         course_name TEXT,
# #         UNIQUE(student_id, course_name),
# #         FOREIGN KEY(course_name) REFERENCES courses(name)
# #     )''')

# #     conn.commit()
# #     conn.close()

# # setup_database()

# # # Admin keyboard
# # def admin_menu():
# #     return ReplyKeyboardMarkup(
# #         [
# #             ["➕ Add Course", "🗑 Delete Course"],
# #             ["📤 Upload Video or PDF"],
# #             ["📂 View Courses", "⬅ Back to Menu"]
# #         ],
# #         resize_keyboard=True
# #     )

# # # Student keyboard
# # def student_menu():
# #     return ReplyKeyboardMarkup(
# #         [["📖 Explore Courses", "📚 My Courses"]],
# #         resize_keyboard=True
# #     )

# # async def start(update: Update, context: CallbackContext) -> None:
# #     user_id = update.message.from_user.id

# #     if user_id in ADMINS:
# #         await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
# #     else:
# #         STUDENTS.add(user_id)
# #         await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())

# # # ➕ Add Course Flow
# # async def add_course(update: Update, context: CallbackContext) -> int:
# #     await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
# #     return ADDING_COURSE

# # async def save_course(update: Update, context: CallbackContext) -> int:
# #     course_name = update.message.text.strip()
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()

# #     try:
# #         cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
# #         conn.commit()
# #         await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
# #     except sqlite3.IntegrityError:
# #         await update.message.reply_text("⚠ Course already exists.")

# #     conn.close()
# #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# #     return ConversationHandler.END

# # # 🗑 Delete Course Flow
# # async def delete_course(update: Update, context: CallbackContext) -> int:
# #     await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
# #     return DELETING_COURSE

# # async def confirm_delete(update: Update, context: CallbackContext) -> int:
# #     course_name = update.message.text.strip()
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()

# #     cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
# #     conn.commit()
# #     conn.close()

# #     await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
# #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# #     return ConversationHandler.END

# # # 📤 Upload Video or PDF Flow
# # async def select_course(update: Update, context: CallbackContext) -> int:
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT name FROM courses")
# #     courses = [row[0] for row in cursor.fetchall()]
# #     conn.close()

# #     if not courses:
# #         await update.message.reply_text("⚠ No courses available. Please add a course first.")
# #         return ConversationHandler.END

# #     course_buttons = [[course] for course in courses]
# #     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

# #     await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
# #     return SELECTING_COURSE

# # async def upload_file(update: Update, context: CallbackContext) -> int:
# #     context.user_data["selected_course"] = update.message.text.strip()
# #     await update.message.reply_text("📤 Send the video or PDF file:")
# #     return UPLOADING_FILE

# # async def save_file(update: Update, context: CallbackContext) -> int:
# #     file = update.message.video or update.message.document
# #     file_id = file.file_id
# #     file_type = "video" if update.message.video else "pdf"
# #     course_name = context.user_data["selected_course"]

# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
# #     conn.commit()
# #     conn.close()

# #     await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
# #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# #     return ConversationHandler.END

# # # 📂 View Courses
# # async def view_courses(update: Update, context: CallbackContext) -> None:
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT name FROM courses")
# #     courses = [row[0] for row in cursor.fetchall()]

# #     if not courses:
# #         await update.message.reply_text("⚠ No courses available.")
# #     else:
# #         message = "📂 Available Courses:\n"
# #         for course in courses:
# #             message += f"\n📌 {course}\n"
# #             cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
# #             files = cursor.fetchall()
# #             for file_type, file_id in files:
# #                 file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
# #                 message += f"  - {file_type_display}: {file_id}\n"

# #     conn.close()
# #     await update.message.reply_text(message)

# # # 📖 Explore Courses
# # async def explore_courses(update: Update, context: CallbackContext) -> int:
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT name FROM courses")
# #     courses = [row[0] for row in cursor.fetchall()]
# #     conn.close()

# #     if not courses:
# #         await update.message.reply_text("⚠ No courses available.")
# #         return ConversationHandler.END

# #     course_buttons = [[course] for course in courses]
# #     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

# #     await update.message.reply_text("📖 Select a course to enroll:", reply_markup=reply_markup)
# #     return ENROLLING_COURSE

# # async def enroll_course(update: Update, context: CallbackContext) -> int:
# #     course_name = update.message.text.strip()
# #     user_id = update.message.from_user.id

# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     try:
# #         cursor.execute("INSERT INTO enrollments (student_id, course_name) VALUES (?, ?)", (user_id, course_name))
# #         conn.commit()
# #         await update.message.reply_text(f"✅ Enrolled in '{course_name}' successfully!")
# #     except sqlite3.IntegrityError:
# #         await update.message.reply_text("⚠ You are already enrolled in this course.")

# #     conn.close()
# #     await update.message.reply_text("🎓 Choose an option:", reply_markup=student_menu())
# #     return ConversationHandler.END

# # # 📚 My Courses
# # async def my_courses(update: Update, context: CallbackContext) -> None:
# #     user_id = update.message.from_user.id
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT course_name FROM enrollments WHERE student_id = ?", (user_id,))
# #     courses = [row[0] for row in cursor.fetchall()]
# #     conn.close()

# #     if not courses:
# #         await update.message.reply_text("⚠ You are not enrolled in any courses.")
# #     else:
# #         message = "📚 Your Enrolled Courses:\n" + "\n".join(f"📌 {course}" for course in courses)
# #         await update.message.reply_text(message)

# # # ⬅ Back to Menu
# # async def back_to_menu(update: Update, context: CallbackContext) -> None:
# #     user_id = update.message.from_user.id
# #     if user_id in ADMINS:
# #         await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
# #     else:
# #         await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

# # def main():
# #     app = Application.builder().token(TOKEN).build()

# #     add_course_handler = ConversationHandler(
# #         entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
# #         states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
# #         fallbacks=[]
# #     )

# #     delete_course_handler = ConversationHandler(
# #         entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
# #         states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
# #         fallbacks=[]
# #     )

# #     upload_handler = ConversationHandler(
# #         entry_points=[MessageHandler(filters.Regex("📤 Upload Video or PDF"), select_course)],
# #         states={
# #             SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
# #             UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
# #         },
# #         fallbacks=[]
# #     )

# #     explore_handler = ConversationHandler(
# #         entry_points=[MessageHandler(filters.Regex("📖 Explore Courses"), explore_courses)],
# #         states={ENROLLING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_course)]},
# #         fallbacks=[]
# #     )

# #     app.add_handler(CommandHandler("start", start))
# #     app.add_handler(add_course_handler)
# #     app.add_handler(delete_course_handler)
# #     app.add_handler(upload_handler)
# #     app.add_handler(explore_handler)
# #     app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
# #     app.add_handler(MessageHandler(filters.Regex("📚 My Courses"), my_courses))
# #     app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))

# #     app.run_polling()

# # if __name__ == "__main__":
# #     main()



# # # import sqlite3
# # # from telegram import (
# # #     Update, 
# # #     ReplyKeyboardMarkup, 
# # #     KeyboardButton, 
# # #     ReplyKeyboardRemove
# # # )
# # # from telegram.ext import (
# # #     Application, 
# # #     CommandHandler, 
# # #     MessageHandler, 
# # #     filters, 
# # #     CallbackContext, 
# # #     ConversationHandler
# # # )

# # # TOKEN = "7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE"  # Replace with your actual bot token
# # # DB_PATH = "courses.db"

# # # # Define user roles
# # # ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
# # # STUDENTS = set()
# # # users_contact_shared = set()  # Store users who have shared contact

# # # # Conversation states
# # # ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE, ENROLLING_COURSE = range(5)

# # # # Database setup
# # # def setup_database():
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()

# # #     cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
# # #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #         name TEXT UNIQUE
# # #     )''')

# # #     cursor.execute('''CREATE TABLE IF NOT EXISTS files (
# # #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #         course_name TEXT,
# # #         file_type TEXT,
# # #         file_id TEXT,
# # #         FOREIGN KEY(course_name) REFERENCES courses(name)
# # #     )''')

# # #     cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
# # #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #         student_id INTEGER,
# # #         course_name TEXT,
# # #         UNIQUE(student_id, course_name),
# # #         FOREIGN KEY(course_name) REFERENCES courses(name)
# # #     )''')

# # #     conn.commit()
# # #     conn.close()

# # # setup_database()

# # # # Admin keyboard
# # # def admin_menu():
# # #     return ReplyKeyboardMarkup(
# # #         [
# # #             ["➕ Add Course", "🗑 Delete Course"],
# # #             ["📤 Upload Video or PDF"],
# # #             ["📂 View Courses", "⬅ Back to Menu"]
# # #         ],
# # #         resize_keyboard=True
# # #     )

# # # # Student keyboard
# # # def student_menu():
# # #     return ReplyKeyboardMarkup(
# # #         [["📖 Explore Courses", "📚 My Courses"]],
# # #         resize_keyboard=True
# # #     )

# # # async def start(update: Update, context: CallbackContext) -> None:
# # #     user_id = update.message.from_user.id
# # #     chat_id = update.message.chat_id

# # #     if user_id in users_contact_shared:
# # #         # User already shared contact, remove keyboard and allow normal messages
# # #         await update.message.reply_text(
# # #             "Welcome back! You have already shared your contact. You can now send messages.",
# # #             reply_markup=ReplyKeyboardRemove()
# # #         )
# # #     else:
# # #         # Send welcome image with caption
# # #         await context.bot.send_photo(
# # #             chat_id=chat_id,
# # #             photo="C:/Users/abget/Downloads/welcome.jpg",  # Replace with actual image URL or local file
# # #             caption="👋 Welcome to the bot! Please share your contact to continue."
# # #         )

# # #         # Show ONLY the "Share My Contact" button with no text input field at all
# # #         contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
# # #         reply_markup = ReplyKeyboardMarkup(
# # #             contact_button, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder=" "
# # #         )

# # #         await update.message.reply_text(" ", reply_markup=reply_markup)

# # # async def contact_handler(update: Update, context: CallbackContext) -> None:
# # #     user = update.message.from_user
# # #     contact = update.message.contact
# # #     user_id = user.id

# # #     if contact:
# # #         phone_number = contact.phone_number
# # #         username = user.username if user.username else "No username"

# # #         # Save user as having shared contact
# # #         users_contact_shared.add(user_id)

# # #         # Remove button and allow free chatting
# # #         await update.message.reply_text(
# # #             f"✅ Contact received!\n\n📞 Phone: {phone_number}\n👤 Username: {username}\n\nYou can now send messages.",
# # #             reply_markup=ReplyKeyboardRemove()
# # #         )

# # # async def block_messages(update: Update, context: CallbackContext) -> None:
# # #     user_id = update.message.from_user.id

# # #     if user_id not in users_contact_shared:
# # #         await update.message.reply_text("⚠️ You must share your contact first! Please press the '📲 Share My Contact' button.")
# # #         return  # Stop further processing

# # # # ➕ Add Course Flow
# # # async def add_course(update: Update, context: CallbackContext) -> int:
# # #     await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
# # #     return ADDING_COURSE

# # # async def save_course(update: Update, context: CallbackContext) -> int:
# # #     course_name = update.message.text.strip()
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()

# # #     try:
# # #         cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
# # #         conn.commit()
# # #         await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
# # #     except sqlite3.IntegrityError:
# # #         await update.message.reply_text("⚠ Course already exists.")

# # #     conn.close()
# # #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# # #     return ConversationHandler.END

# # # # 🗑 Delete Course Flow
# # # async def delete_course(update: Update, context: CallbackContext) -> int:
# # #     await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
# # #     return DELETING_COURSE

# # # async def confirm_delete(update: Update, context: CallbackContext) -> int:
# # #     course_name = update.message.text.strip()
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()

# # #     cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
# # #     conn.commit()
# # #     conn.close()

# # #     await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
# # #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# # #     return ConversationHandler.END

# # # # 📤 Upload Video or PDF Flow
# # # async def select_course(update: Update, context: CallbackContext) -> int:
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT name FROM courses")
# # #     courses = [row[0] for row in cursor.fetchall()]
# # #     conn.close()

# # #     if not courses:
# # #         await update.message.reply_text("⚠ No courses available. Please add a course first.")
# # #         return ConversationHandler.END

# # #     course_buttons = [[course] for course in courses]
# # #     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

# # #     await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
# # #     return SELECTING_COURSE

# # # async def upload_file(update: Update, context: CallbackContext) -> int:
# # #     context.user_data["selected_course"] = update.message.text.strip()
# # #     await update.message.reply_text("📤 Send the video or PDF file:")
# # #     return UPLOADING_FILE

# # # async def save_file(update: Update, context: CallbackContext) -> int:
# # #     file = update.message.video or update.message.document
# # #     file_id = file.file_id
# # #     file_type = "video" if update.message.video else "pdf"
# # #     course_name = context.user_data["selected_course"]

# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
# # #     conn.commit()
# # #     conn.close()

# # #     await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
# # #     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
# # #     return ConversationHandler.END

# # # # 📂 View Courses
# # # async def view_courses(update: Update, context: CallbackContext) -> None:
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT name FROM courses")
# # #     courses = [row[0] for row in cursor.fetchall()]

# # #     if not courses:
# # #         await update.message.reply_text("⚠ No courses available.")
# # #     else:
# # #         message = "📂 Available Courses:\n"
# # #         for course in courses:
# # #             message += f"\n📌 {course}\n"
# # #             cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
# # #             files = cursor.fetchall()
# # #             for file_type, file_id in files:
# # #                 file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
# # #                 message += f"  - {file_type_display}: {file_id}\n"

# # #     conn.close()
# # #     await update.message.reply_text(message)

# # # # 📖 Explore Courses
# # # async def explore_courses(update: Update, context: CallbackContext) -> int:
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT name FROM courses")
# # #     courses = [row[0] for row in cursor.fetchall()]
# # #     conn.close()

# # #     if not courses:
# # #         await update.message.reply_text("⚠ No courses available.")
# # #         return ConversationHandler.END

# # #     course_buttons = [[course] for course in courses]
# # #     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

# # #     await update.message.reply_text("📖 Select a course to enroll:", reply_markup=reply_markup)
# # #     return ENROLLING_COURSE

# # # async def enroll_course(update: Update, context: CallbackContext) -> int:
# # #     course_name = update.message.text.strip()
# # #     user_id = update.message.from_user.id

# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     try:
# # #         cursor.execute("INSERT INTO enrollments (student_id, course_name) VALUES (?, ?)", (user_id, course_name))
# # #         conn.commit()
# # #         await update.message.reply_text(f"✅ Enrolled in '{course_name}' successfully!")
# # #     except sqlite3.IntegrityError:
# # #         await update.message.reply_text("⚠ You are already enrolled in this course.")

# # #     conn.close()
# # #     await update.message.reply_text("🎓 Choose an option:", reply_markup=student_menu())
# # #     return ConversationHandler.END

# # # # 📚 My Courses
# # # async def my_courses(update: Update, context: CallbackContext) -> None:
# # #     user_id = update.message.from_user.id
# # #     conn = sqlite3.connect(DB_PATH)
# # #     cursor = conn.cursor()
# # #     cursor.execute("SELECT course_name FROM enrollments WHERE student_id = ?", (user_id,))
# # #     courses = [row[0] for row in cursor.fetchall()]
# # #     conn.close()

# # #     if not courses:
# # #         await update.message.reply_text("⚠ You are not enrolled in any courses.")
# # #     else:
# # #         message = "📚 Your Enrolled Courses:\n" + "\n".join(f"📌 {course}" for course in courses)
# # #         await update.message.reply_text(message)

# # # # ⬅ Back to Menu
# # # async def back_to_menu(update: Update, context: CallbackContext) -> None:
# # #     user_id = update.message.from_user.id
# # #     if user_id in ADMINS:
# # #         await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
# # #     else:
# # #         await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

# # # def main():
# # #     app = Application.builder().token(TOKEN).build()

# # #     add_course_handler = ConversationHandler(
# # #         entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
# # #         states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
# # #         fallbacks=[]
# # #     )

# # #     delete_course_handler = ConversationHandler(
# # #         entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
# # #         states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
# # #         fallbacks=[]
# # #     )

# # #     upload_handler = ConversationHandler(
# # #         entry_points=[MessageHandler(filters.Regex("📤 Upload Video or PDF"), select_course)],
# # #         states={
# # #             SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
# # #             UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
# # #         },
# # #         fallbacks=[]
# # #     )

# # #     explore_handler = ConversationHandler(
# # #         entry_points=[MessageHandler(filters.Regex("📖 Explore Courses"), explore_courses)],
# # #         states={ENROLLING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_course)]},
# # #         fallbacks=[]
# # #     )

# # #     app.add_handler(CommandHandler("start", start))
# # #     app.add_handler(add_course_handler)
# # #     app.add_handler(delete_course_handler)
# # #     app.add_handler(upload_handler)
# # #     app.add_handler(explore_handler)
# # #     app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
# # #     app.add_handler(MessageHandler(filters.Regex("📚 My Courses"), my_courses))
# # #     app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))
# # #     app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
# # #     app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))  # Block all messages except contact

# # #     app.run_polling()

# # # if __name__ == "__main__":
# # #     main()



# import sqlite3
# from telegram import (
#     Update, 
#     ReplyKeyboardMarkup, 
#     KeyboardButton, 
#     ReplyKeyboardRemove
# )
# from telegram.ext import (
#     Application, 
#     CommandHandler, 
#     MessageHandler, 
#     filters, 
#     CallbackContext, 
#     ConversationHandler
# )

# TOKEN = "7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE"  # Replace with your actual bot token
# DB_PATH = "courses.db"

# # Define user roles
# ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
# STUDENTS = set()
# users_contact_shared = set()  # Store users who have shared contact

# # Conversation states
# ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE, ENROLLING_COURSE = range(5)

# # Database setup
# def setup_database():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS files (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         course_name TEXT,
#         file_type TEXT,
#         file_id TEXT,
#         FOREIGN KEY(course_name) REFERENCES courses(name)
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         student_id INTEGER,
#         course_name TEXT,
#         UNIQUE(student_id, course_name),
#         FOREIGN KEY(course_name) REFERENCES courses(name)
#     )''')

#     conn.commit()
#     conn.close()

# setup_database()

# # Admin keyboard
# def admin_menu():
#     return ReplyKeyboardMarkup(
#         [
#             ["➕ Add Course", "🗑 Delete Course"],
#             ["📤 Upload Video or PDF"],
#             ["📂 View Courses", "⬅ Back to Menu"]
#         ],
#         resize_keyboard=True
#     )

# # Student keyboard
# def student_menu():
#     return ReplyKeyboardMarkup(
#         [["📖 Explore Courses", "📚 My Courses"]],
#         resize_keyboard=True
#     )

# async def start(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user_id = update.message.from_user.id

#     if user_id in users_contact_shared:
#         await update.message.reply_text('Welcome back!', reply_markup=ReplyKeyboardRemove())
#     else:
#         await context.bot.send_photo(
#             chat_id=chat_id,
#             photo="C:/Users/abget/Downloads/welcome.jpg",  # Replace with actual image URL or local file
#             caption="Hello, welcome to Venturemeda!"
#         )

#         # Create "Share My Contact" button
#         contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
#         reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

#         # Send the new button
#         await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)

# async def contact_handler(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     contact = update.message.contact
#     user_id = user.id

#     if contact:
#         phone_number = contact.phone_number
#         username = user.username if user.username else "No username"

#         users_contact_shared.add(user_id)

#         # Send user contact details
#         await update.message.reply_text(
#             f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
#             reply_markup=ReplyKeyboardRemove()
#         )

# async def block_messages(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id not in users_contact_shared:
#         await update.message.reply_text("You must share your contact first please press the share my contact button.")
#         return

# # ➕ Add Course Flow
# async def add_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
#     return ADDING_COURSE

# async def save_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     try:
#         cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
#         conn.commit()
#         await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
#     except sqlite3.IntegrityError:
#         await update.message.reply_text("⚠ Course already exists.")

#     conn.close()
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 🗑 Delete Course Flow
# async def delete_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
#     return DELETING_COURSE

# async def confirm_delete(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📤 Upload Video or PDF Flow
# async def select_course(update: Update, context: CallbackContext) -> int:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ No courses available. Please add a course first.")
#         return ConversationHandler.END

#     course_buttons = [[course] for course in courses]
#     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

#     await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
#     return SELECTING_COURSE

# async def upload_file(update: Update, context: CallbackContext) -> int:
#     context.user_data["selected_course"] = update.message.text.strip()
#     await update.message.reply_text("📤 Send the video or PDF file:")
#     return UPLOADING_FILE

# async def save_file(update: Update, context: CallbackContext) -> int:
#     file = update.message.video or update.message.document
#     file_id = file.file_id
#     file_type = "video" if update.message.video else "pdf"
#     course_name = context.user_data["selected_course"]

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📂 View Courses
# async def view_courses(update: Update, context: CallbackContext) -> None:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]

#     if not courses:
#         await update.message.reply_text("⚠ No courses available.")
#     else:
#         message = "📂 Available Courses:\n"
#         for course in courses:
#             message += f"\n📌 {course}\n"
#             cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
#             files = cursor.fetchall()
#             for file_type, file_id in files:
#                 file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
#                 message += f"  - {file_type_display}: {file_id}\n"

#     conn.close()
#     await update.message.reply_text(message)

# # 📖 Explore Courses
# async def explore_courses(update: Update, context: CallbackContext) -> int:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ No courses available.")
#         return ConversationHandler.END

#     course_buttons = [[course] for course in courses]
#     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

#     await update.message.reply_text("📖 Select a course to enroll:", reply_markup=reply_markup)
#     return ENROLLING_COURSE

# async def enroll_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     user_id = update.message.from_user.id

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO enrollments (student_id, course_name) VALUES (?, ?)", (user_id, course_name))
#         conn.commit()
#         await update.message.reply_text(f"✅ Enrolled in '{course_name}' successfully!")
#     except sqlite3.IntegrityError:
#         await update.message.reply_text("⚠ You are already enrolled in this course.")

#     conn.close()
#     await update.message.reply_text("🎓 Choose an option:", reply_markup=student_menu())
#     return ConversationHandler.END

# # 📚 My Courses
# async def my_courses(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT course_name FROM enrollments WHERE student_id = ?", (user_id,))
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ You are not enrolled in any courses.")
#     else:
#         message = "📚 Your Enrolled Courses:\n" + "\n".join(f"📌 {course}" for course in courses)
#         await update.message.reply_text(message)

# # ⬅ Back to Menu
# async def back_to_menu(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id in ADMINS:
#         await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
#     else:
#         await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

# def main():
#     app = Application.builder().token(TOKEN).build()

#     add_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
#         states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
#         fallbacks=[]
#     )

#     delete_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
#         states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
#         fallbacks=[]
#     )

#     upload_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("📤 Upload Video or PDF"), select_course)],
#         states={
#             SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
#             UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
#         },
#         fallbacks=[]
#     )

#     explore_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("📖 Explore Courses"), explore_courses)],
#         states={ENROLLING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_course)]},
#         fallbacks=[]
#     )

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(add_course_handler)
#     app.add_handler(delete_course_handler)
#     app.add_handler(upload_handler)
#     app.add_handler(explore_handler)
#     app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
#     app.add_handler(MessageHandler(filters.Regex("📚 My Courses"), my_courses))
#     app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))
#     app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
#     app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))  # Block all messages except contact

#     app.run_polling()

# if __name__ == "__main__":
#     main()



# import sqlite3
# from telegram import (
#     Update, 
#     ReplyKeyboardMarkup, 
#     KeyboardButton, 
#     ReplyKeyboardRemove
# )
# from telegram.ext import (
#     Application, 
#     CommandHandler, 
#     MessageHandler, 
#     filters, 
#     CallbackContext, 
#     ConversationHandler
# )

# TOKEN = "7823854850:AAGwcumdHLpdZXdtlTMbO8Et4oH4CZLkQdE"  # Replace with your actual bot token
# DB_PATH = "courses.db"

# # Define user roles
# ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
# STUDENTS = set()
# users_contact_shared = set()  # Store users who have shared contact

# # Conversation states
# ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE, ENROLLING_COURSE = range(5)

# # Database setup
# def setup_database():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT UNIQUE
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS files (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         course_name TEXT,
#         file_type TEXT,
#         file_id TEXT,
#         FOREIGN KEY(course_name) REFERENCES courses(name)
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         student_id INTEGER,
#         course_name TEXT,
#         UNIQUE(student_id, course_name),
#         FOREIGN KEY(course_name) REFERENCES courses(name)
#     )''')

#     conn.commit()
#     conn.close()

# setup_database()

# # Admin keyboard
# def admin_menu():
#     return ReplyKeyboardMarkup(
#         [
#             ["➕ Add Course", "🗑 Delete Course"],
#             ["📤 Upload Video or PDF"],
#             ["📂 View Courses", "⬅ Back to Menu"]
#         ],
#         resize_keyboard=True
#     )

# # Student keyboard
# def student_menu():
#     return ReplyKeyboardMarkup(
#         [["📖 Explore Courses", "📚 My Courses"]],
#         resize_keyboard=True
#     )

# async def start(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user_id = update.message.from_user.id

#     if user_id in users_contact_shared:
#         if user_id in ADMINS:
#             await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
#         else:
#             STUDENTS.add(user_id)
#             await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())
#     else:
#         await context.bot.send_photo(
#             chat_id=chat_id,
#             photo="C:/Users/abget/Downloads/welcome.jpg",  # Replace with actual image URL or local file
#             caption="Hello, welcome to Venturemeda! Please share your contact to continue."
#         )

#         # Create "Share My Contact" button
#         contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
#         reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

#         # Send the new button
#         await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)

# async def contact_handler(update: Update, context: CallbackContext) -> None:
#     user = update.message.from_user
#     contact = update.message.contact
#     user_id = user.id

#     if contact:
#         phone_number = contact.phone_number
#         username = user.username if user.username else "No username"

#         users_contact_shared.add(user_id)

#         # Send user contact details
#         await update.message.reply_text(
#             f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
#             reply_markup=ReplyKeyboardRemove()
#         )

#         # Direct user to the appropriate menu
#         if user_id in ADMINS:
#             await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
#         else:
#             STUDENTS.add(user_id)
#             await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())

# async def block_messages(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id not in users_contact_shared:
#         await update.message.reply_text("You must share your contact first please press the share my contact button.")
#         return

# # ➕ Add Course Flow
# async def add_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
#     return ADDING_COURSE

# async def save_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     try:
#         cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
#         conn.commit()
#         await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
#     except sqlite3.IntegrityError:
#         await update.message.reply_text("⚠ Course already exists.")

#     conn.close()
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 🗑 Delete Course Flow
# async def delete_course(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
#     return DELETING_COURSE

# async def confirm_delete(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📤 Upload Video or PDF Flow
# async def select_course(update: Update, context: CallbackContext) -> int:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ No courses available. Please add a course first.")
#         return ConversationHandler.END

#     course_buttons = [[course] for course in courses]
#     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

#     await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
#     return SELECTING_COURSE

# async def upload_file(update: Update, context: CallbackContext) -> int:
#     context.user_data["selected_course"] = update.message.text.strip()
#     await update.message.reply_text("📤 Send the video or PDF file:")
#     return UPLOADING_FILE

# async def save_file(update: Update, context: CallbackContext) -> int:
#     file = update.message.video or update.message.document
#     file_id = file.file_id
#     file_type = "video" if update.message.video else "pdf"
#     course_name = context.user_data["selected_course"]

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
#     conn.commit()
#     conn.close()

#     await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
#     await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
#     return ConversationHandler.END

# # 📂 View Courses
# async def view_courses(update: Update, context: CallbackContext) -> None:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]

#     if not courses:
#         await update.message.reply_text("⚠ No courses available.")
#     else:
#         message = "📂 Available Courses:\n"
#         for course in courses:
#             message += f"\n📌 {course}\n"
#             cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
#             files = cursor.fetchall()
#             for file_type, file_id in files:
#                 file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
#                 message += f"  - {file_type_display}: {file_id}\n"

#     conn.close()
#     await update.message.reply_text(message)

# # 📖 Explore Courses
# async def explore_courses(update: Update, context: CallbackContext) -> int:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM courses")
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ No courses available.")
#         return ConversationHandler.END

#     course_buttons = [[course] for course in courses]
#     reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

#     await update.message.reply_text("📖 Select a course to enroll:", reply_markup=reply_markup)
#     return ENROLLING_COURSE

# async def enroll_course(update: Update, context: CallbackContext) -> int:
#     course_name = update.message.text.strip()
#     user_id = update.message.from_user.id

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO enrollments (student_id, course_name) VALUES (?, ?)", (user_id, course_name))
#         conn.commit()
#         await update.message.reply_text(f"✅ Enrolled in '{course_name}' successfully!")
#     except sqlite3.IntegrityError:
#         await update.message.reply_text("⚠ You are already enrolled in this course.")

#     conn.close()
#     await update.message.reply_text("🎓 Choose an option:", reply_markup=student_menu())
#     return ConversationHandler.END

# # 📚 My Courses
# async def my_courses(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT course_name FROM enrollments WHERE student_id = ?", (user_id,))
#     courses = [row[0] for row in cursor.fetchall()]
#     conn.close()

#     if not courses:
#         await update.message.reply_text("⚠ You are not enrolled in any courses.")
#     else:
#         message = "📚 Your Enrolled Courses:\n" + "\n".join(f"📌 {course}" for course in courses)
#         await update.message.reply_text(message)

# # ⬅ Back to Menu
# async def back_to_menu(update: Update, context: CallbackContext) -> None:
#     user_id = update.message.from_user.id
#     if user_id in ADMINS:
#         await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
#     else:
#         await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

# def main():
#     app = Application.builder().token(TOKEN).build()

#     add_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
#         states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
#         fallbacks=[]
#     )

#     delete_course_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
#         states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
#         fallbacks=[]
#     )

#     upload_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("📤 Upload Video or PDF"), select_course)],
#         states={
#             SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
#             UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
#         },
#         fallbacks=[]
#     )

#     explore_handler = ConversationHandler(
#         entry_points=[MessageHandler(filters.Regex("📖 Explore Courses"), explore_courses)],
#         states={ENROLLING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_course)]},
#         fallbacks=[]
#     )

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(add_course_handler)
#     app.add_handler(delete_course_handler)
#     app.add_handler(upload_handler)
#     app.add_handler(explore_handler)
#     app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
#     app.add_handler(MessageHandler(filters.Regex("📚 My Courses"), my_courses))
#     app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))
#     app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
#     app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))  # Block all messages except contact

#     app.run_polling()

# if __name__ == "__main__":
#     main()
