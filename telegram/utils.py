import asyncio

import httpx

from utils.apis import send_exam_result
from .serializers import CreateTelegramUserSerializer
from environs import Env

from utils.loader import db_bot as db

env = Env()
env.read_env()

token = env.str("BOT_TOKEN")

MESSAGES = {
    'uz': {
        'DRAFT': "⚠️ Arizangiz qoralama holatida. Iltimos, tekshirib, arizangizni yuboring.",
        'SUBMITTED': "☑️ Arizangiz tekshirishga yuborildi. Iltimos, tasdiqlanishini kuting.",
        'REJECTED': "❌ Arizangiz rad etildi. Iltimos, kiritilgan ma'lumotlarni tekshirib, arizangizni qaytadan yuboring.",
        'ACCEPTED': "✅ Arizangiz qabul qilindi. Quyidagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosib, imtihon topshirishingiz mumkin!",
        'EXAMINED': "🔄 Imtihon topshirilgan. Iltimos, natijasini kuting.",
        'FAILED': "😔 Afsuski imtihondan o'ta olmadingiz. Sizga yana bir imkoniyat beriladi. Buning uchun quyidagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosing.",
        'PASSED': "🥳 Tabriklaymiz! Siz Fan va texnologiyalar universitetiga tavsiya etildingiz. Shartnomani ko'chirib olish uchun pastda \"Shartnomani olish\" tugmasini bosing. Savollaringiz bo’lsa bizga qo’ng’iroq qiling: 78-888-38-88",
        'PASSED_DTM': "🥳 Tabriklaymiz, siz imtihonsiz, UZBMB (DTM) natijangiz asosida Fan va texnologiyalar universitetiga talabalikka tavsiya etildingiz! Shartnomani ko'chirib olish uchun pastda \"Shartnomani olish\" tugmasini bosing. Savollaringiz bo’lsa bizga qo’ng’iroq qiling: 78-888-38-88",
    },
    'ru': {
        'DRAFT': "⚠️ Ваша заявка находится в черновике. Пожалуйста, проверьте и отправьте вашу заявку.",
        'SUBMITTED': "☑️ Ваша заявка отправлена на проверку. Пожалуйста, ожидайте подтверждения.",
        'REJECTED': "❌ Ваша заявка отклонена. Пожалуйста, проверьте введенные данные и отправьте заявку повторно.",
        'ACCEPTED': "✅ Ваша заявка принята. Вы можете сдать экзамен, нажав на кнопку \"🧑‍💻 Сдать экзамен\" ниже!",
        'EXAMINED': "🔄 Экзамен сдан. Пожалуйста, ожидайте результатов.",
        'FAILED': "😔 К сожалению, вы не прошли экзамен. Вам будет предоставлена еще одна возможность. Для этого нажмите кнопку \"🧑‍💻 Сдать экзамен\" ниже.",
        'PASSED': "🥳 Поздравляем! Вы рекомендованы к зачислению в Университет науки и технологий. Чтобы скачать контракт, нажмите кнопку \"📥 Получить контракт\" ниже. Если у вас есть вопросы, позвоните нам: 78-888-38-88",
        'PASSED_DTM': "🥳 Поздравляем, вы успешно прошли экзамен! На основе результатов UZBMB (DTM) вы рекомендованы к зачислению в Университет науки и технологий. Чтобы скачать контракт, нажмите кнопку \"📥 Получить контракт\" ниже. Если у вас есть вопросы, позвоните нам: 78-888-38-88",

    },
    'en': {
        'DRAFT': "⚠️ Your application is in draft status. Please review and submit your application.",
        'SUBMITTED': "☑️ Your application has been submitted for review. Please wait for confirmation.",
        'REJECTED': "❌ Your application was rejected. Please check the entered information and resubmit your application.",
        'ACCEPTED': "✅ Your application has been accepted. You can take the exam by clicking the \"🧑‍💻 Take the exam\" button below!",
        'EXAMINED': "🔄 The exam has been submitted. Please wait for the results.",
        'FAILED': "😔 Unfortunately, you did not pass the exam. You will be given another opportunity. To do this, click the \"🧑‍💻 Take the exam\" button below.",
        'PASSED': "🥳 Congratulations! You have been recommended for admission to the University of Science and Technology. To download the contract, click the \"Get Contract\" button below. If you have any questions, please call us at: 78-888-38-88",
        'PASSED_DTM': "🥳 Congratulations, you have passed the exam! Based on your UZBMB (DTM) results, you have been recommended for admission to the University of Science and Technology. To download the contract, click the \"Get Contract\" button below. If you have any questions, please call us at: 78-888-38-88",
    }
}


async def send_message_via_tg_api(telegram_user: CreateTelegramUserSerializer):
    tg_id = telegram_user.validated_data['tg_id']
    status = telegram_user.validated_data['status']
    lang = telegram_user.validated_data.get('lang', 'uz')

    text = get_message_text(tg_id, lang, status)
    if text:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {
            'chat_id': tg_id,
            'text': text
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, sync_send_message, url, params)


def sync_send_message(url, params):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message(url, params))


async def send_message(url, params):
    async with httpx.AsyncClient() as client:
        await client.get(url, params=params)


def get_message_text(tgId, lang, status):
    applicant = db.get_application_status(tgId)

    if applicant:
        db.update_application_status(tgId, status)

        if status == 'PASSED' and applicant['status'] == 'SUBMITTED':
            status = 'PASSED_DTM'
        elif status == 'ACCEPTED' and applicant['status'] == 'EXAMINED':
            exam_result = db.get_exam_result(tgId)
            if exam_result:
                send_exam_result(tgId, str(exam_result['totalScore']))
                status = 'EXAMINED'
                db.update_application_status(tgId, status)
                return None

    return MESSAGES.get(lang, {}).get(status, "Unknown status")

