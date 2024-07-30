import httpx

from .serializers import CreateTelegramUserSerializer
from environs import Env

env = Env()
env.read_env()

token = env.str("BOT_TOKEN")

MESSAGES = {
    'uz': {
        'DRAFT': "⚠️ Arizangiz qoralama holatida. Iltimos, tekshirib, arizangizni yuboring.",
        'SUBMITTED': "☑️ Arizangiz tekshirishga yuborildi. Iltimos, tasdiqlanishini kuting.",
        'REJECTED': "❌ Arizangiz rad etildi. Iltimos, kiritilgan ma'lumotlarni tekshirib, arizangizni qaytadan yuboring.",
        'ACCEPTED': "✅ Arizangiz qabul qilindi. Quyidagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosib, imtihon topshirishingiz mumkin!",
        'EXAMINED': "🔄 Imtihon topshirildi. Iltimos, natijasini kuting.",
        'FAILED': "😔 Afsuski imtihondan o'ta olmadingiz. Sizga yana bir imkoniyat beriladi. Buning uchun quyidagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosing.",
        'PASSED': "🥳 Tabriklaymiz! Siz Fan va texnologiyalar universitetiga tavsiya etildingiz. Quyidagi \"📥 Shartnomani olish\" tugmasi orqali shartnomani yuklab olishingiz mumkin.",
    },
    'ru': {
        'DRAFT': "⚠️ Ваша заявка находится в черновике. Пожалуйста, проверьте и отправьте вашу заявку.",
        'SUBMITTED': "☑️ Ваша заявка отправлена на проверку. Пожалуйста, ожидайте подтверждения.",
        'REJECTED': "❌ Ваша заявка отклонена. Пожалуйста, проверьте введенные данные и отправьте заявку повторно.",
        'ACCEPTED': "✅ Ваша заявка принята. Вы можете сдать экзамен, нажав на кнопку \"🧑‍💻 Сдать экзамен\" ниже!",
        'EXAMINED': "🔄 Экзамен сдан. Пожалуйста, ожидайте результат.",
        'FAILED': "😔 К сожалению, вы не прошли экзамен. Вам будет предоставлена еще одна возможность. Для этого нажмите кнопку \"🧑‍💻 Сдать экзамен\" ниже.",
        'PASSED': "🥳 Поздравляем! Вы рекомендованы в Университет науки и технологий. Вы можете скачать договор, нажав на кнопку \"📥 Получить договор\" ниже.",
    },
    'en': {
        'DRAFT': "⚠️ Your application is in draft status. Please review and submit your application.",
        'SUBMITTED': "☑️ Your application has been submitted for review. Please wait for confirmation.",
        'REJECTED': "❌ Your application was rejected. Please check the entered information and resubmit your application.",
        'ACCEPTED': "✅ Your application has been accepted. You can take the exam by clicking the \"🧑‍💻 Take the exam\" button below!",
        'EXAMINED': "🔄 The exam has been taken. Please wait for the results.",
        'FAILED': "😔 Unfortunately, you did not pass the exam. You will be given another opportunity. To do this, click the \"🧑‍💻 Take the exam\" button below.",
        'PASSED': "🥳 Congratulations! You have been recommended to the University of Science and Technology. You can download the contract by clicking the \"📥 Get the contract\" button below.",
    }
}


async def send_message_via_tg_api(telegram_user: CreateTelegramUserSerializer):
    tg_id = telegram_user.validated_data['tg_id']
    status = telegram_user.validated_data['status']
    lang = telegram_user.validated_data.get('lang', 'uz')

    text = MESSAGES.get(lang, {}).get(status, "Unknown status")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        'chat_id': tg_id,
        'text': text
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        return {"message": "Message sent successfully"}
    else:
        return {"message": "Failed to send message", "details": response.json()}
