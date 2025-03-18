import sqlite3
import os
from dotenv import load_dotenv
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackContext, 
    ConversationHandler
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Replace with your actual bot token
DB_PATH = os.getenv("DB_PATH")

# Define user roles
ADMINS = {314589754}  # Replace with actual admin Telegram user IDs
STUDENTS = set()
users_contact_shared = set()  # Store users who have shared contact

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in the .env file")
if not DB_PATH:
    raise ValueError("DB_PATH is not set in the .env file")


# Conversation states
ADDING_COURSE, DELETING_COURSE, SELECTING_COURSE, UPLOADING_FILE, ENROLLING_COURSE = range(5)

# Database setup
def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        file_type TEXT,
        file_id TEXT,
        FOREIGN KEY(course_name) REFERENCES courses(name)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_name TEXT,
        UNIQUE(student_id, course_name),
        FOREIGN KEY(course_name) REFERENCES courses(name)
    )''')

    conn.commit()
    conn.close()

setup_database()

# Admin keyboard
def admin_menu():
    return ReplyKeyboardMarkup(
        [
            ["➕ Add Course", "🗑 Delete Course"],
            ["📤 Upload Video or PDF"],
            ["📂 View Courses", "⬅ Back to Menu"]
        ],
        resize_keyboard=True
    )

# Student keyboard
def student_menu():
    return ReplyKeyboardMarkup(
        [["📖 Explore Courses", "📚 My Courses"]],
        resize_keyboard=True
    )

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if user_id in users_contact_shared:
        if user_id in ADMINS:
            await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
        else:
            STUDENTS.add(user_id)
            await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo="C:/Users/abget/Downloads/welcome.jpg",  # Replace with actual image URL or local file
            caption="Hello, welcome to Venturemeda! Please share your contact to continue."
        )

        # Create "Share My Contact" button
        contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True)

        # Send the new button
        await update.message.reply_text("Please share your contact info:", reply_markup=reply_markup)

async def contact_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    contact = update.message.contact
    user_id = user.id

    if contact:
        phone_number = contact.phone_number
        username = user.username if user.username else "No username"

        users_contact_shared.add(user_id)

        # Send user contact details
        await update.message.reply_text(
            f"Thank you! Here is your info:\n📞 Phone: {phone_number}\n👤 Username: {username}",
            reply_markup=ReplyKeyboardRemove()
        )

        # Direct user to the appropriate menu
        if user_id in ADMINS:
            await update.message.reply_text("👑 Welcome, Admin! Choose an action:", reply_markup=admin_menu())
        else:
            STUDENTS.add(user_id)
            await update.message.reply_text("🎓 Welcome, Student! Choose an option:", reply_markup=student_menu())

async def block_messages(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in users_contact_shared:
        await update.message.reply_text("You must share your contact first please press the share my contact button.")
        return

# ➕ Add Course Flow
async def add_course(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Enter the course name:", reply_markup=ReplyKeyboardRemove())
    return ADDING_COURSE

async def save_course(update: Update, context: CallbackContext) -> int:
    course_name = update.message.text.strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO courses (name) VALUES (?)", (course_name,))
        conn.commit()
        await update.message.reply_text(f"✅ Course '{course_name}' added successfully!")
    except sqlite3.IntegrityError:
        await update.message.reply_text("⚠ Course already exists.")

    conn.close()
    await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
    return ConversationHandler.END

# 🗑 Delete Course Flow
async def delete_course(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Enter the course name to delete:", reply_markup=ReplyKeyboardRemove())
    return DELETING_COURSE

async def confirm_delete(update: Update, context: CallbackContext) -> int:
    course_name = update.message.text.strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM courses WHERE name = ?", (course_name,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Course '{course_name}' deleted successfully!")
    await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
    return ConversationHandler.END

# 📤 Upload Video or PDF Flow
async def select_course(update: Update, context: CallbackContext) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM courses")
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not courses:
        await update.message.reply_text("⚠ No courses available. Please add a course first.")
        return ConversationHandler.END

    course_buttons = [[course] for course in courses]
    reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

    await update.message.reply_text("📂 Select a course:", reply_markup=reply_markup)
    return SELECTING_COURSE

async def upload_file(update: Update, context: CallbackContext) -> int:
    context.user_data["selected_course"] = update.message.text.strip()
    await update.message.reply_text("📤 Send the video or PDF file:")
    return UPLOADING_FILE

async def save_file(update: Update, context: CallbackContext) -> int:
    file = update.message.video or update.message.document
    file_id = file.file_id
    file_type = "video" if update.message.video else "pdf"
    course_name = context.user_data["selected_course"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (course_name, file_type, file_id) VALUES (?, ?, ?)", (course_name, file_type, file_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ {file_type.upper()} added to '{course_name}' successfully!")
    await update.message.reply_text("👑 Choose an action:", reply_markup=admin_menu())
    return ConversationHandler.END

# 📂 View Courses
async def view_courses(update: Update, context: CallbackContext) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM courses")
    courses = [row[0] for row in cursor.fetchall()]

    if not courses:
        await update.message.reply_text("⚠ No courses available.")
    else:
        message = "📂 Available Courses:\n"
        for course in courses:
            message += f"\n📌 {course}\n"
            cursor.execute("SELECT file_type, file_id FROM files WHERE course_name = ?", (course,))
            files = cursor.fetchall()
            for file_type, file_id in files:
                file_type_display = "📹 Video" if file_type == "video" else "📄 PDF"
                message += f"  - {file_type_display}: {file_id}\n"

    conn.close()
    await update.message.reply_text(message)

# 📖 Explore Courses
async def explore_courses(update: Update, context: CallbackContext) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM courses")
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not courses:
        await update.message.reply_text("⚠ No courses available.")
        return ConversationHandler.END

    course_buttons = [[course] for course in courses]
    reply_markup = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

    await update.message.reply_text("📖 Select a course to enroll:", reply_markup=reply_markup)
    return ENROLLING_COURSE

async def enroll_course(update: Update, context: CallbackContext) -> int:
    course_name = update.message.text.strip()
    user_id = update.message.from_user.id

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_name) VALUES (?, ?)", (user_id, course_name))
        conn.commit()
        await update.message.reply_text(f"✅ Enrolled in '{course_name}' successfully!")
    except sqlite3.IntegrityError:
        await update.message.reply_text("⚠ You are already enrolled in this course.")

    conn.close()
    await update.message.reply_text("🎓 Choose an option:", reply_markup=student_menu())
    return ConversationHandler.END

# 📚 My Courses
async def my_courses(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT course_name FROM enrollments WHERE student_id = ?", (user_id,))
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not courses:
        await update.message.reply_text("⚠ You are not enrolled in any courses.")
    else:
        message = "📚 Your Enrolled Courses:\n" + "\n".join(f"📌 {course}" for course in courses)
        await update.message.reply_text(message)

# ⬅ Back to Menu
async def back_to_menu(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in ADMINS:
        await update.message.reply_text("👑 Admin Menu:", reply_markup=admin_menu())
    else:
        await update.message.reply_text("🎓 Student Menu:", reply_markup=student_menu())

def main():
    app = Application.builder().token(TOKEN).build()

    add_course_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("➕ Add Course"), add_course)],
        states={ADDING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_course)]},
        fallbacks=[]
    )

    delete_course_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🗑 Delete Course"), delete_course)],
        states={DELETING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)]},
        fallbacks=[]
    )

    upload_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📤 Upload Video or PDF"), select_course)],
        states={
            SELECTING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, upload_file)],
            UPLOADING_FILE: [MessageHandler(filters.Document.ALL | filters.VIDEO, save_file)]
        },
        fallbacks=[]
    )

    explore_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📖 Explore Courses"), explore_courses)],
        states={ENROLLING_COURSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enroll_course)]},
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(add_course_handler)
    app.add_handler(delete_course_handler)
    app.add_handler(upload_handler)
    app.add_handler(explore_handler)
    app.add_handler(MessageHandler(filters.Regex("📂 View Courses"), view_courses))
    app.add_handler(MessageHandler(filters.Regex("📚 My Courses"), my_courses))
    app.add_handler(MessageHandler(filters.Regex("⬅ Back to Menu"), back_to_menu))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))  # Block all messages except contact

    app.run_polling()

if __name__ == "__main__":
    main()