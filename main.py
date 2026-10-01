import os
import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
import yt_dlp

BOT_TOKEN = "8919352024:AAEY-feyDhJicLMEO8Ezx0FBlc2LR0Q-yXY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Har qanday xabarni qabul qilish uchun (tekshirish)
@dp.message()
async def handle_all_messages(message: types.Message):
    # Agar start bosilsa
    if message.text == "/start":
        await message.answer("Salom! Bot muvaffaqiyatli ishga tushdi! 🚀\nMenga Instagram, TikTok yoki YouTube havolasini yuboring.")
        return

    # Agar xabar link (http) bo'lsa
    if message.text and message.text.startswith("http"):
        url = message.text.strip()
        status_msg = await message.answer("Video yuklanmoqda, kuting... ⏳")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloaded_video.%(ext)s',
            'quiet': True,
        }

        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
            
            video_file = None
            for file in os.listdir('.'):
                if file.startswith('downloaded_video.'):
                    video_file = file
                    break
                    
            if video_file and os.path.exists(video_file):
                video = types.FSInputFile(video_file)
                await message.answer_video(video, caption="Mana sizning videongiz! 🎬")
                os.remove(video_file)
                await status_msg.delete()
            else:
                await status_msg.edit_text("Videoni yuklab bo'lmadi.")

        except Exception as e:
            await status_msg.edit_text(f"Xatolik yuz berdi: {str(e)}")
    else:
        await message.answer("Menga faqat video havolasini (link) yuboring!")

async def main():
    # Eski PuzzleBot kabi barcha webhooklarni to'liq o'chirish
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
