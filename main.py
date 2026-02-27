"""
🎓 DTM Test Generator Bot — Single File Version
Server uchun tayyor | aiogram 3.x
"""

import asyncio
import random
import os
from datetime import datetime

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ══════════════════════════════════════════════════
#                    CONFIG
# ══════════════════════════════════════════════════
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

SUBJECTS = {
    "math":    {"name": "📐 Matematika", "emoji": "📐"},
    "uzbek":   {"name": "📖 Ona tili",   "emoji": "📖"},
    "history": {"name": "🏛️ Tarix",      "emoji": "🏛️"},
    "english": {"name": "🌍 Ingliz tili","emoji": "🌍"},
}

# ══════════════════════════════════════════════════
#                  SAVOLLAR BAZASI
# ══════════════════════════════════════════════════
QUESTIONS_DB = {
    "math": [
        {"q": "2² + 3² = ?", "options": ["10", "12", "13", "15"], "answer": 2, "explanation": "4 + 9 = 13"},
        {"q": "√144 = ?", "options": ["11", "12", "13", "14"], "answer": 1, "explanation": "12 × 12 = 144"},
        {"q": "200 ning 15% ini toping", "options": ["25", "30", "35", "40"], "answer": 1, "explanation": "200 × 0.15 = 30"},
        {"q": "Agar x + 5 = 12 bo'lsa, x = ?", "options": ["5", "6", "7", "8"], "answer": 2, "explanation": "x = 12 - 5 = 7"},
        {"q": "3! (faktorial) = ?", "options": ["3", "6", "9", "12"], "answer": 1, "explanation": "3! = 3 × 2 × 1 = 6"},
        {"q": "log₁₀(1000) = ?", "options": ["2", "3", "4", "5"], "answer": 1, "explanation": "10³ = 1000"},
        {"q": "sin(90°) = ?", "options": ["0", "0.5", "1", "√2/2"], "answer": 2, "explanation": "sin(90°) = 1"},
        {"q": "Trapetsiya yuzi: asoslari 6 va 10, balandligi 4", "options": ["32", "36", "40", "48"], "answer": 0, "explanation": "S = (6+10)/2 × 4 = 32"},
        {"q": "2x - 3 = 7, x = ?", "options": ["4", "5", "6", "7"], "answer": 1, "explanation": "2x = 10, x = 5"},
        {"q": "π ≈ ?", "options": ["3.14", "3.41", "3.12", "3.16"], "answer": 0, "explanation": "π ≈ 3.14159..."},
        {"q": "4³ = ?", "options": ["12", "48", "64", "81"], "answer": 2, "explanation": "4 × 4 × 4 = 64"},
        {"q": "|-7| = ?", "options": ["-7", "0", "7", "49"], "answer": 2, "explanation": "Modul har doim musbat"},
        {"q": "Tomonlari 3, 4, 5 bo'lgan uchburchak qanday?", "options": ["O'tmas", "O'tkir", "To'g'ri burchakli", "Teng tomonli"], "answer": 2, "explanation": "3²+4²=5² → to'g'ri burchakli"},
        {"q": "1 km = ? metr", "options": ["10", "100", "1000", "10000"], "answer": 2, "explanation": "1 km = 1000 m"},
        {"q": "2, 4, 6, 8, 10 — o'rtacha = ?", "options": ["5", "6", "7", "8"], "answer": 1, "explanation": "30 / 5 = 6"},
        {"q": "Doira yuzi: r=7, π=3.14", "options": ["43.96", "153.86", "43.86", "154"], "answer": 1, "explanation": "S = π × r² = 3.14 × 49 ≈ 153.86"},
        {"q": "(-3)² = ?", "options": ["-9", "-6", "6", "9"], "answer": 3, "explanation": "(-3)×(-3) = 9"},
        {"q": "a:b = 2:3, a=8 bo'lsa, b=?", "options": ["10", "12", "14", "16"], "answer": 1, "explanation": "b = 8 × 3/2 = 12"},
        {"q": "0.5 × 0.5 = ?", "options": ["0.1", "0.25", "0.5", "1"], "answer": 1, "explanation": "0.5 × 0.5 = 0.25"},
        {"q": "Kvadrat perimetri: tomon 5", "options": ["10", "15", "20", "25"], "answer": 2, "explanation": "P = 4 × 5 = 20"},
        {"q": "cos(0°) = ?", "options": ["0", "0.5", "1", "-1"], "answer": 2, "explanation": "cos(0°) = 1"},
        {"q": "7 × 8 = ?", "options": ["54", "56", "58", "60"], "answer": 1, "explanation": "7 × 8 = 56"},
        {"q": "Yig'indisi 20, farqi 4. Katta son = ?", "options": ["10", "11", "12", "13"], "answer": 2, "explanation": "x+y=20, x-y=4 → x=12"},
        {"q": "2^10 = ?", "options": ["512", "1024", "2048", "256"], "answer": 1, "explanation": "2^10 = 1024"},
        {"q": "v=60 km/h, t=2.5 soat. Masofa = ?", "options": ["120", "140", "150", "160"], "answer": 2, "explanation": "S = 60 × 2.5 = 150 km"},
        {"q": "1/3 + 1/6 = ?", "options": ["1/2", "2/9", "1/3", "2/3"], "answer": 0, "explanation": "2/6 + 1/6 = 3/6 = 1/2"},
        {"q": "25% oshirilganda 100 bo'ldi. Dastlabki son?", "options": ["70", "75", "80", "85"], "answer": 2, "explanation": "x × 1.25 = 100 → x = 80"},
        {"q": "tan(45°) = ?", "options": ["0", "0.5", "1", "√3"], "answer": 2, "explanation": "tan(45°) = 1"},
        {"q": "5! = ?", "options": ["60", "100", "120", "150"], "answer": 2, "explanation": "5×4×3×2×1 = 120"},
        {"q": "p(x) = x²-5x+6, p(2) = ?", "options": ["0", "2", "4", "6"], "answer": 0, "explanation": "4 - 10 + 6 = 0"},
    ],
    "uzbek": [
        {"q": "'Bahor' so'zining sinonimi?", "options": ["Qish", "Yoz", "Ko'klam", "Kuz"], "answer": 2, "explanation": "Ko'klam = Bahor"},
        {"q": "Ko'plik qo'shimchasi qaysi?", "options": ["-li", "-lar", "-mi", "-da"], "answer": 1, "explanation": "-lar ko'plik bildiradi"},
        {"q": "'Ota-ona' qaysi so'z turkumi?", "options": ["Fe'l", "Ot", "Sifat", "Ravish"], "answer": 1, "explanation": "Ota-ona — ot"},
        {"q": "'Go'zal' antonimi?", "options": ["Chiroyli", "Xunuk", "Kelishgan", "Qo'pol"], "answer": 1, "explanation": "Go'zal ↔ Xunuk"},
        {"q": "Qaysi so'z sifat?", "options": ["Kitob", "Yurmoq", "Qizil", "Tez"], "answer": 2, "explanation": "Qizil — belgi bildiruvchi sifat"},
        {"q": "Unli harflar nechtа?", "options": ["4", "5", "6", "7"], "answer": 2, "explanation": "O'zbek tilida 6 ta unli: a, e, i, o, u, o'"},
        {"q": "Fe'lning inkor qo'shimchasi?", "options": ["-ma", "-mi", "-cha", "-lar"], "answer": 0, "explanation": "-ma: borma, kelma"},
        {"q": "'Toshkent' so'zida nechta bo'g'in?", "options": ["1", "2", "3", "4"], "answer": 1, "explanation": "Tosh-kent — 2 bo'g'in"},
        {"q": "Ravish nimani bildiradi?", "options": ["Predmet", "Belgi", "Harakat holati", "Son"], "answer": 2, "explanation": "Ravish harakat holatini bildiradi"},
        {"q": "Gapning asosiy bo'laklari?", "options": ["Ega va kesim", "To'ldiruvchi va hol", "Aniqlovchi va hol", "Ega va to'ldiruvchi"], "answer": 0, "explanation": "Ega va kesim — grammatik asos"},
        {"q": "'Kitobxona' qanday yasalgan?", "options": ["Qo'shma", "Juft", "Affiksli", "Qisqartma"], "answer": 2, "explanation": "Kitob + xona (affiksli)"},
        {"q": "Qaysi gap oddiy gap?", "options": ["Men o'qiyman va sen yozasan", "Havo yaxshi.", "Agar kelsa, aytaman", "U keldi, men ketdim"], "answer": 1, "explanation": "'Havo yaxshi' — bir kesimli oddiy gap"},
        {"q": "Qaysi so'zda imlo xatosi bor?", "options": ["Qo'shiq", "Ko'cha", "Toshkent", "Yuldus"], "answer": 3, "explanation": "To'g'risi: Yulduz"},
        {"q": "Old qo'shimcha (prefiks) qaysi so'zda?", "options": ["Bog'cha", "Bebaho", "Bolalik", "Ishchi"], "answer": 1, "explanation": "Be- — prefiks"},
        {"q": "I shaxs birlik egalik qo'shimchasi?", "options": ["-im", "-ing", "-i", "-imiz"], "answer": 0, "explanation": "Men → -im (kitobim)"},
        {"q": "So'roq olmoshlari?", "options": ["Men, sen, u", "Kim, nima, qaysi", "Bu, shu, o'sha", "Hamma, har"], "answer": 1, "explanation": "Kim? Nima? Qaysi?"},
        {"q": "Qaysi so'z undov?", "options": ["Oh!", "U", "Ko'k", "Bordi"], "answer": 0, "explanation": "Oh! — his-tuyg'u undovi"},
        {"q": "'Alpomish' dostonining janri?", "options": ["Lirik", "Epik", "Dramatik", "Satirik"], "answer": 1, "explanation": "Alpomish — qahramonlik eposi"},
        {"q": "Uyushiq bo'laklar qaysi gapda?", "options": ["U keldi.", "Ali va Vali o'ynashdi.", "Men kitob o'qidim.", "Havo sovuq."], "answer": 1, "explanation": "Ali va Vali — uyushiq egalar"},
        {"q": "Fe'l o'tgan zamon qo'shimchasi?", "options": ["-adi", "-di", "-sa", "-moq"], "answer": 1, "explanation": "-di: keldi, bordi"},
        {"q": "Qaysi so'z son?", "options": ["Ko'p", "Besh", "Oz", "Bir oz"], "answer": 1, "explanation": "Besh — miqdor son"},
        {"q": "'Mehnat' ma'nosi?", "options": ["Dam olish", "Ish qilish", "O'rganish", "Sayohat"], "answer": 1, "explanation": "Mehnat = ish, emak"},
        {"q": "To'liqsiz gap nima?", "options": ["Egasi yo'q gap", "Ikki bo'lagi yo'q gap", "Biri tushirilgan gap", "Ko'p kesimli gap"], "answer": 2, "explanation": "Bir bo'lak tushirib qoldiriladi"},
        {"q": "Ot yasovchi qo'shimcha?", "options": ["-li", "-chi", "-roq", "-cha"], "answer": 1, "explanation": "-chi: ishchi, o'quvchi"},
        {"q": "Paronim nima?", "options": ["Ma'nodosh so'z", "Qarama-qarshi so'z", "Talaffuzi o'xshash so'z", "Ko'p ma'noli so'z"], "answer": 2, "explanation": "Talaffuzi o'xshash, ma'nosi farqli"},
        {"q": "Qaysi gap to'g'ri yozilgan?", "options": ["kitobni o'qi.", "Kitob'ni o'qi", "Kitobni o'qi.", "kitobni O'qi"], "answer": 2, "explanation": "Bosh harf + nuqta"},
        {"q": "'Bilim — nur' gapida nechta so'z?", "options": ["1", "2", "3", "4"], "answer": 1, "explanation": "Bilim, nur — 2 ta so'z"},
        {"q": "Qaysi so'z olmosh?", "options": ["Katta", "Bordi", "Men", "Tez"], "answer": 2, "explanation": "Men — shaxs olmoshi"},
        {"q": "Muloqot undovlari?", "options": ["Assalomu alaykum, xayr", "Kitob, daftar", "Bordi, keldi", "Yaxshi, chiroyli"], "answer": 0, "explanation": "Assalomu alaykum, xayr — muloqot undovlari"},
        {"q": "'Mehribon' qaysi turkum?", "options": ["Ot", "Fe'l", "Sifat", "Ravish"], "answer": 2, "explanation": "Mehribon — sifat (belgi bildiradi)"},
    ],
    "history": [
        {"q": "O'zbekiston mustaqillikka qachon erishdi?", "options": ["1990", "1991", "1992", "1993"], "answer": 1, "explanation": "1991-yil 1-sentabr — Mustaqillik kuni"},
        {"q": "Amir Temur qachon tug'ilgan?", "options": ["1330", "1336", "1340", "1350"], "answer": 1, "explanation": "1336-yil 9-aprel"},
        {"q": "Buyuk Ipak yo'li qaysi davlatlarni bog'lagan?", "options": ["Xitoy–Rim", "Hindiston–Misr", "Eron–Gretsiya", "Arabiston–Hindiston"], "answer": 0, "explanation": "Xitoydan Rimgacha"},
        {"q": "Al-Xorazmiy algebrani qaysi asarda yaratdi?", "options": ["Kanon", "Kitob ul-jabr", "Ziyj", "Tuhfat"], "answer": 1, "explanation": "'Al-Kitob al-muxtasar fi hisob al-jabr'"},
        {"q": "Temuriylar poytaxti?", "options": ["Buxoro", "Samarqand", "Xiva", "Qo'qon"], "answer": 1, "explanation": "Samarqand — Amir Temur poytaxti"},
        {"q": "O'zbekistonning birinchi prezidenti?", "options": ["Shavkat Mirziyoyev", "Islom Karimov", "Abdulhashim Mutalov", "Asliddin Xo'jaev"], "answer": 1, "explanation": "Islom Karimov"},
        {"q": "I Jahon urushi qachon boshlangan?", "options": ["1912", "1914", "1916", "1918"], "answer": 1, "explanation": "1914-yil"},
        {"q": "Qoraxoniylar qachon tashkil topgan?", "options": ["840", "940", "1040", "1140"], "answer": 0, "explanation": "840-yilda"},
        {"q": "Ibn Sino asosiy asari?", "options": ["Ziyj", "Kanon at-tib", "Muqaddima", "Devoni hikmat"], "answer": 1, "explanation": "'Al-Qonun fit-tib' — tibbiyot qomusi"},
        {"q": "Aleksandr Makedonskiy O'rta Osiyoga qachon kirdi?", "options": ["333 yil.av", "329 yil.av", "323 yil.av", "310 yil.av"], "answer": 1, "explanation": "329 yil avv."},
        {"q": "II Jahon urushi qachon tugadi?", "options": ["1944", "1945", "1946", "1947"], "answer": 1, "explanation": "1945-yil 9-may (Yevropa)"},
        {"q": "O'zbekiston Konstitutsiyasi qachon qabul qilingan?", "options": ["1991", "1992", "1993", "1994"], "answer": 1, "explanation": "1992-yil 8-dekabr"},
        {"q": "Navoiy qaysi shahrida tug'ilgan?", "options": ["Samarqand", "Buxoro", "Hirot", "Toshkent"], "answer": 2, "explanation": "1441-yilda Hirotda"},
        {"q": "O'rta asrlar Markaziy Osiyoda qaysi din hukmron?", "options": ["Xristianlik", "Buddizm", "Islom", "Zardo'shtiylik"], "answer": 2, "explanation": "VII asrdan Islom"},
        {"q": "Samarqand qachon asos solingan?", "options": ["2000 yil avv", "2500 yil avv", "3000 yil avv", "1500 yil avv"], "answer": 1, "explanation": "2500+ yil tarix"},
        {"q": "Mo'g'ul imperiyasini kim asos solgan?", "options": ["Og'edeyxon", "Qubilayxon", "Chingizxon", "Botixon"], "answer": 2, "explanation": "Chingizxon 1206-yilda"},
        {"q": "Toshkent metro qachon ochildi?", "options": ["1975", "1977", "1979", "1981"], "answer": 1, "explanation": "1977-yilda"},
        {"q": "19-asrda Markaziy Osiyoni kim bosib oldi?", "options": ["Britaniya", "Fransiya", "Rossiya", "Xitoy"], "answer": 2, "explanation": "Rossiya imperiyasi"},
        {"q": "Ulug'bek rasadxonasi qayerda?", "options": ["Toshkent", "Buxoro", "Samarqand", "Farg'ona"], "answer": 2, "explanation": "Samarqandda (1428-29 yy)"},
        {"q": "Birinchi kosmosga chiqqan inson?", "options": ["Neil Armstrong", "Yuriy Gagarin", "Buzz Aldrin", "Alan Shepard"], "answer": 1, "explanation": "1961-yil 12-aprel"},
        {"q": "Navro'z qachon?", "options": ["21-fevral", "8-mart", "21-mart", "1-may"], "answer": 2, "explanation": "21-mart — bahor tengkechasi"},
        {"q": "Buxoro amirligini kim tugatdi?", "options": ["Rossiya imperiyasi", "Qizil Armiya", "Britaniya", "Eron"], "answer": 1, "explanation": "1920-yilda Qizil Armiya"},
        {"q": "O'zbek so'mi qachon kiritildi?", "options": ["1991", "1993", "1994", "1995"], "answer": 1, "explanation": "1993-yil 1-iyul"},
        {"q": "'Sharqning Pariji' deb atalgan shahar?", "options": ["Buxoro", "Samarqand", "Toshkent", "Xiva"], "answer": 1, "explanation": "Samarqand"},
        {"q": "Amir Temur qayerda dafn etilgan?", "options": ["Shahrisabz", "Samarqand", "Buxoro", "Toshkent"], "answer": 1, "explanation": "Samarqand — Go'ri Amir"},
        {"q": "O'zbekiston nechta ma'muriy birlikdan iborat?", "options": ["11", "12", "13", "14"], "answer": 3, "explanation": "12 viloyat + QQR + Toshkent sh. = 14"},
        {"q": "Berdaq — qaysi xalqning shoiri?", "options": ["O'zbek", "Qozoq", "Qoraqalpoq", "Tojik"], "answer": 2, "explanation": "Qoraqalpog'iston ulug' shoiri"},
        {"q": "SSSR qachon tarqaldi?", "options": ["1989", "1990", "1991", "1992"], "answer": 2, "explanation": "1991-yil 25-dekabr"},
        {"q": "Xiva xonligi qachon tashkil topgan?", "options": ["1511", "1551", "1601", "1701"], "answer": 0, "explanation": "1511-yilda"},
        {"q": "O'rta Osiyo respublikalari qachon sovetlashdi?", "options": ["1918-1920", "1920-1924", "1924-1930", "1930-1936"], "answer": 1, "explanation": "1920-1924 yillar"},
    ],
    "english": [
        {"q": "Past tense of 'go'?", "options": ["goed", "went", "gone", "going"], "answer": 1, "explanation": "go → went (irregular verb)"},
        {"q": "___ apple a day keeps the doctor away", "options": ["a", "an", "the", "—"], "answer": 1, "explanation": "'an' — unli oldidan"},
        {"q": "Plural of 'child'?", "options": ["childs", "childes", "children", "child's"], "answer": 2, "explanation": "child → children"},
        {"q": "She ___ to school every day.", "options": ["go", "goes", "going", "went"], "answer": 1, "explanation": "she/he/it + goes"},
        {"q": "'Beautiful' nimani bildiradi?", "options": ["Xunuk", "Go'zal", "Kuchli", "Tez"], "answer": 1, "explanation": "Beautiful = go'zal"},
        {"q": "Opposite of 'hot'?", "options": ["warm", "cool", "cold", "mild"], "answer": 2, "explanation": "hot ↔ cold"},
        {"q": "Which is correct?", "options": ["I am going yesterday", "I went yesterday", "I go yesterday", "I was go"], "answer": 1, "explanation": "yesterday → past → went"},
        {"q": "Letters in English alphabet?", "options": ["24", "25", "26", "27"], "answer": 2, "explanation": "26 ta harf"},
        {"q": "Capital of England?", "options": ["Manchester", "Birmingham", "London", "Liverpool"], "answer": 2, "explanation": "London"},
        {"q": "'Kitob stol ustida' = ?", "options": ["under the table", "on the table", "near the table", "behind the table"], "answer": 1, "explanation": "ustida = on"},
        {"q": "I ___ a student.", "options": ["am", "is", "are", "be"], "answer": 0, "explanation": "I + am"},
        {"q": "Synonym of 'big'?", "options": ["small", "tiny", "large", "little"], "answer": 2, "explanation": "big = large"},
        {"q": "She has ___ books.", "options": ["much", "many", "a lot", "lots"], "answer": 1, "explanation": "books = countable → many"},
        {"q": "Yesterday I ___ a movie.", "options": ["watch", "watched", "watching", "watches"], "answer": 1, "explanation": "Yesterday → past → watched"},
        {"q": "'Library' nimani bildiradi?", "options": ["Kutubxona", "Do'kon", "Shifoxona", "Maktab"], "answer": 0, "explanation": "Library = kutubxona"},
        {"q": "They ___ playing football now.", "options": ["is", "am", "are", "be"], "answer": 2, "explanation": "They + are"},
        {"q": "Which word is a verb?", "options": ["beautiful", "quickly", "run", "table"], "answer": 2, "explanation": "run — fe'l"},
        {"q": "If I had money, I ___ buy a car.", "options": ["would", "will", "shall", "can"], "answer": 0, "explanation": "2nd conditional → would"},
        {"q": "Which is NOT a preposition?", "options": ["on", "in", "run", "under"], "answer": 2, "explanation": "run — fe'l, qolganlar predlog"},
        {"q": "'Water' plural?", "options": ["waters", "water", "wateres", "watery"], "answer": 1, "explanation": "water — uncountable"},
        {"q": "She is ___ than her sister.", "options": ["tall", "taller", "tallest", "most tall"], "answer": 1, "explanation": "than → comparative → taller"},
        {"q": "I ___ been to London.", "options": ["have", "has", "had", "did"], "answer": 0, "explanation": "I + have (Present Perfect)"},
        {"q": "'Exhausted' nimani bildiradi?", "options": ["Xursand", "Qo'rqqan", "Charchagan", "Hayron"], "answer": 2, "explanation": "Exhausted = juda charchagan"},
        {"q": "Correctly spelled?", "options": ["recieve", "receive", "recive", "receeve"], "answer": 1, "explanation": "i before e except after c → receive"},
        {"q": "Tomorrow ___ sunny.", "options": ["is", "was", "will be", "were"], "answer": 2, "explanation": "Tomorrow → future → will be"},
        {"q": "The movie was ___.", "options": ["boring", "boringly", "bored", "boredness"], "answer": 0, "explanation": "narsa ta'rifida → boring"},
        {"q": "I haven't seen him ___ Monday.", "options": ["for", "since", "from", "during"], "answer": 1, "explanation": "Aniq vaqtdan beri → since"},
        {"q": "3rd form of 'write'?", "options": ["writed", "wrote", "written", "writing"], "answer": 2, "explanation": "write → wrote → written"},
        {"q": "She suggested ___ early.", "options": ["leave", "to leave", "leaving", "left"], "answer": 2, "explanation": "suggest + -ing"},
        {"q": "How do you say '5:30'?", "options": ["five thirty", "half five", "Both A&B", "five and half"], "answer": 2, "explanation": "five thirty yoki half past five"},
    ],
}

# ══════════════════════════════════════════════════
#                 STATES & USER DATA
# ══════════════════════════════════════════════════
class TestState(StatesGroup):
    choosing_subject = State()
    choosing_count   = State()
    in_test          = State()

user_data        = {}
error_statistics = {}

def get_user(uid: int) -> dict:
    if uid not in user_data:
        user_data[uid] = {
            "subject": None, "count": 10, "current_q": 0,
            "answers": [], "questions": [], "score": 0,
            "total_tests": 0, "total_correct": 0,
        }
    return user_data[uid]

# ══════════════════════════════════════════════════
#                   KEYBOARDS
# ══════════════════════════════════════════════════
def kb_main():
    b = InlineKeyboardBuilder()
    b.button(text="🚀 Test Boshlash", callback_data="start_test")
    b.button(text="📊 Statistikam",   callback_data="my_stats")
    b.button(text="❓ Yordam",        callback_data="help")
    b.adjust(1)
    return b.as_markup()

def kb_subjects():
    b = InlineKeyboardBuilder()
    for key, val in SUBJECTS.items():
        b.button(text=val["name"], callback_data=f"subj_{key}")
    b.button(text="🔙 Orqaga", callback_data="back_main")
    b.adjust(2, 2, 1)
    return b.as_markup()

def kb_count():
    b = InlineKeyboardBuilder()
    for c in [10, 20, 30]:
        b.button(text=f"📝 {c} ta savol", callback_data=f"cnt_{c}")
    b.button(text="🔙 Orqaga", callback_data="back_subj")
    b.adjust(3, 1)
    return b.as_markup()

def kb_answers(idx: int):
    b = InlineKeyboardBuilder()
    for i, ltr in enumerate(["A", "B", "C", "D"]):
        b.button(text=ltr, callback_data=f"ans_{idx}_{i}")
    b.adjust(4)
    return b.as_markup()

def kb_result(subject: str):
    b = InlineKeyboardBuilder()
    b.button(text="🔄 Qaytadan shu fandan", callback_data=f"retry_{subject}")
    b.button(text="📚 Boshqa fan",          callback_data="start_test")
    b.button(text="📊 Statistikam",         callback_data="my_stats")
    b.button(text="🏠 Bosh menyu",          callback_data="back_main")
    b.adjust(1, 1, 2)
    return b.as_markup()

# ══════════════════════════════════════════════════
#                   HANDLERS
# ══════════════════════════════════════════════════

# ── /start ───────────────────────────────────────
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"🎓 *Assalomu alaykum, {message.from_user.first_name}!*\n\n"
        "🏆 *DTM Test Generator*ga xush kelibsiz!\n\n"
        "📚 *Fanlar:* Matematika · Ona tili · Tarix · Ingliz tili\n"
        "📝 *Test hajmi:* 10 / 20 / 30 ta savol\n"
        "✅ Har javobdan keyin izoh ko'rsatiladi!\n\n"
        "Boshlash uchun tugmani bosing 👇",
        reply_markup=kb_main(), parse_mode="Markdown"
    )

# ── Test boshlash ─────────────────────────────────
async def on_start_test(cb: CallbackQuery, state: FSMContext):
    await state.set_state(TestState.choosing_subject)
    await cb.message.edit_text(
        "📚 *Qaysi fandan test topshirmoqchisiz?*",
        reply_markup=kb_subjects(), parse_mode="Markdown"
    )
    await cb.answer()

async def on_subject(cb: CallbackQuery, state: FSMContext):
    subject = cb.data.split("_")[1]
    await state.update_data(subject=subject)
    await state.set_state(TestState.choosing_count)
    await cb.message.edit_text(
        f"✅ *{SUBJECTS[subject]['name']}* tanlandi!\n\n📝 Nechta savol?",
        reply_markup=kb_count(), parse_mode="Markdown"
    )
    await cb.answer()

async def on_count(cb: CallbackQuery, state: FSMContext):
    count   = int(cb.data.split("_")[1])
    subject = (await state.get_data())["subject"]
    qs      = random.sample(QUESTIONS_DB[subject], min(count, len(QUESTIONS_DB[subject])))

    uid = cb.from_user.id
    ud  = get_user(uid)
    ud.update(subject=subject, count=len(qs), current_q=0,
              answers=[], questions=qs, score=0, start_time=datetime.now())

    await state.set_state(TestState.in_test)
    await cb.message.edit_text(
        f"🚀 *Test boshlanmoqda!*\n\n"
        f"📚 {SUBJECTS[subject]['name']}  |  📝 {len(qs)} ta savol\n\n"
        "Omad! 🍀", parse_mode="Markdown"
    )
    await asyncio.sleep(1.2)
    await _send_question(cb.message, qs, 0)
    await cb.answer()

# ── Savol yuborish ────────────────────────────────
async def _send_question(msg: Message, questions: list, idx: int):
    q     = questions[idx]
    total = len(questions)
    bar   = "🟩" * idx + "⬜" * (total - idx)
    if total > 15:
        bar = f"{'🟩' * idx} {idx}/{total}"

    opts = "\n".join(
        f"{['🅰️','🅱️','🅲','🅳'][i]} {opt}"
        for i, opt in enumerate(q["options"])
    )
    await msg.answer(
        f"📊 *{idx + 1} / {total}*\n{bar}\n\n❓ *{q['q']}*\n\n{opts}",
        reply_markup=kb_answers(idx), parse_mode="Markdown"
    )

# ── Javob qabul qilish ────────────────────────────
async def on_answer(cb: CallbackQuery, state: FSMContext):
    _, idx_s, ans_s = cb.data.split("_")
    idx, user_ans   = int(idx_s), int(ans_s)

    uid = cb.from_user.id
    ud  = get_user(uid)

    if len(ud["answers"]) > idx:
        await cb.answer("Allaqachon javob berdingiz!", show_alert=True)
        return

    q       = ud["questions"][idx]
    correct = q["answer"]
    ok      = user_ans == correct
    ud["answers"].append(user_ans)

    if ok:
        ud["score"] += 1
    else:
        key = f"{ud['subject']}_{idx}"
        error_statistics.setdefault(uid, {})
        error_statistics[uid][key] = error_statistics[uid].get(key, 0) + 1

    L   = ["A", "B", "C", "D"]
    txt = (
        f"{'✅' if ok else '❌'} *{'To\'g\'ri!' if ok else 'Noto\'g\'ri!'}*\n\n"
        f"Javobingiz: *{L[user_ans]}) {q['options'][user_ans]}*\n"
    )
    if not ok:
        txt += f"To'g'ri javob: *{L[correct]}) {q['options'][correct]}*\n"
    txt += f"\n💡 *Izoh:* {q['explanation']}"

    await cb.message.edit_text(txt, parse_mode="Markdown")
    await cb.answer("✅ To'g'ri!" if ok else "❌ Xato!")
    await asyncio.sleep(1.5)

    nxt = idx + 1
    if nxt < len(ud["questions"]):
        await _send_question(cb.message, ud["questions"], nxt)
    else:
        ud["total_tests"]   = ud.get("total_tests", 0) + 1
        ud["total_correct"] = ud.get("total_correct", 0) + ud["score"]
        await _send_result(cb.message, ud, uid)

# ── Natija ────────────────────────────────────────
async def _send_result(msg: Message, ud: dict, uid: int):
    score, total = ud["score"], len(ud["questions"])
    pct          = round(score / total * 100)
    subj         = ud["subject"]

    if pct >= 90:   grade, gmsg = "🏆 A'lo (5)",      "DTMga tayyor! 🎉"
    elif pct >= 70: grade, gmsg = "👍 Yaxshi (4)",     "Yana biroz mashq qiling!"
    elif pct >= 50: grade, gmsg = "😐 Qoniqarli (3)",  "Ko'proq urinib ko'ring!"
    else:           grade, gmsg = "😔 Qoniqarsiz (2)", "Mavzularni qayta o'rganing!"

    bar = "🟩" * (pct // 10) + "⬜" * (10 - pct // 10)
    m, s = divmod((datetime.now() - ud.get("start_time", datetime.now())).seconds, 60)

    txt = (
        f"🏁 *TEST YAKUNLANDI!*\n"
        f"{'─'*28}\n"
        f"📚 {SUBJECTS[subj]['name']}\n"
        f"{'─'*28}\n\n"
        f"✅ To'g'ri: *{score}* / {total}\n"
        f"❌ Xato:   *{total - score}*\n"
        f"📊 Foiz:   *{pct}%*\n\n"
        f"{bar}\n\n"
        f"🎯 *{grade}*\n"
        f"💬 {gmsg}\n\n"
        f"⏱ Vaqt: {m} daq {s} son\n\n"
    )

    wrongs = [
        f"• Q{i+1}: {q['q'][:38]}..."
        for i, (q, a) in enumerate(zip(ud["questions"], ud["answers"]))
        if a != q["answer"]
    ]
    if wrongs:
        txt += "❗ *Xato savollar:*\n" + "\n".join(wrongs[:5])
        if len(wrongs) > 5:
            txt += f"\n_...va yana {len(wrongs)-5} ta_"

    await msg.answer(txt, reply_markup=kb_result(subj), parse_mode="Markdown")

# ── Qaytadan ─────────────────────────────────────
async def on_retry(cb: CallbackQuery, state: FSMContext):
    subj  = cb.data.split("_")[1]
    uid   = cb.from_user.id
    ud    = get_user(uid)
    count = ud.get("count", 10)
    qs    = random.sample(QUESTIONS_DB[subj], min(count, len(QUESTIONS_DB[subj])))

    ud.update(subject=subj, count=len(qs), current_q=0,
              answers=[], questions=qs, score=0, start_time=datetime.now())
    await state.set_state(TestState.in_test)
    await cb.message.answer(
        f"🔄 *{SUBJECTS[subj]['name']}* — yangi test!\n📝 {len(qs)} ta savol | Omad! 🍀",
        parse_mode="Markdown"
    )
    await asyncio.sleep(1)
    await _send_question(cb.message, qs, 0)
    await cb.answer()

# ── Statistika ────────────────────────────────────
async def on_stats(cb: CallbackQuery, state: FSMContext):
    uid = cb.from_user.id
    ud  = get_user(uid)
    tt  = ud.get("total_tests", 0)
    tc  = ud.get("total_correct", 0)

    if tt == 0:
        txt = "📊 *Statistika*\n\nHali test topshirmadingiz.\nBoshlang! 🚀"
    else:
        avg = round(tc / (tt * 10) * 100)
        txt = (
            f"📊 *Sizning statistikangiz*\n\n"
            f"🧪 Jami testlar:  *{tt}* ta\n"
            f"✅ Jami to'g'ri:  *{tc}* ta\n"
            f"📈 O'rtacha:      *{avg}%*\n"
        )
        errs = error_statistics.get(uid, {})
        if errs:
            top  = sorted(errs.items(), key=lambda x: -x[1])[:3]
            txt += "\n❗ *Eng ko'p xato:*\n"
            for qkey, cnt in top:
                parts = qkey.split("_")
                subj, qidx = parts[0], int(parts[1])
                try:
                    qtxt = QUESTIONS_DB[subj][qidx]["q"][:38]
                    txt += f"• {SUBJECTS[subj]['emoji']} {qtxt}... ×{cnt}\n"
                except Exception:
                    pass

    b = InlineKeyboardBuilder()
    b.button(text="🚀 Test Boshlash", callback_data="start_test")
    b.button(text="🏠 Bosh menyu",    callback_data="back_main")
    b.adjust(2)
    await cb.message.edit_text(txt, reply_markup=b.as_markup(), parse_mode="Markdown")
    await cb.answer()

# ── Yordam ────────────────────────────────────────
async def on_help(cb: CallbackQuery, state: FSMContext):
    b = InlineKeyboardBuilder()
    b.button(text="🚀 Test Boshlash", callback_data="start_test")
    b.button(text="🏠 Bosh menyu",    callback_data="back_main")
    b.adjust(2)
    await cb.message.edit_text(
        "❓ *Yordam*\n\n"
        "1️⃣ 'Test Boshlash' tugmasini bosing\n"
        "2️⃣ Fan tanlang\n"
        "3️⃣ Savol sonini belgilang (10/20/30)\n"
        "4️⃣ Har savolga A/B/C/D bosing\n"
        "5️⃣ Natijangizni ko'ring!\n\n"
        "💡 Har javobdan keyin izoh beriladi\n"
        "📈 Statistikada xatolaringiz tahlil qilinadi\n\n"
        "🌟 Muvaffaqiyat!",
        reply_markup=b.as_markup(), parse_mode="Markdown"
    )
    await cb.answer()

# ── Navigatsiya ───────────────────────────────────
async def on_back_main(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text(
        f"🏠 *Bosh Menyu*\n\nSalom, *{cb.from_user.first_name}*! Nima qilmoqchisiz?",
        reply_markup=kb_main(), parse_mode="Markdown"
    )
    await cb.answer()

async def on_back_subj(cb: CallbackQuery, state: FSMContext):
    await state.set_state(TestState.choosing_subject)
    await cb.message.edit_text(
        "📚 *Fan tanlang:*", reply_markup=kb_subjects(), parse_mode="Markdown"
    )
    await cb.answer()

# ══════════════════════════════════════════════════
#                     MAIN
# ══════════════════════════════════════════════════
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())

    # Commands
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_start, Command("menu"))

    # Callbacks
    dp.callback_query.register(on_start_test, F.data == "start_test")
    dp.callback_query.register(on_subject,    F.data.startswith("subj_"))
    dp.callback_query.register(on_count,      F.data.startswith("cnt_"))
    dp.callback_query.register(on_answer,     F.data.startswith("ans_"))
    dp.callback_query.register(on_retry,      F.data.startswith("retry_"))
    dp.callback_query.register(on_stats,      F.data == "my_stats")
    dp.callback_query.register(on_help,       F.data == "help")
    dp.callback_query.register(on_back_main,  F.data == "back_main")
    dp.callback_query.register(on_back_subj,  F.data == "back_subj")

    print("━" * 38)
    print("  🎓 DTM Test Generator Bot")
    print("  ✅ Ishga tushdi! | Ctrl+C — to'xtat")
    print("━" * 38)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())