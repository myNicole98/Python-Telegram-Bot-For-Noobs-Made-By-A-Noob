from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, Updater
from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
import json
lang = json.load(open("localization/en_US.json", "r", encoding='utf-8'))

def init(update, context):
    user_id = update.effective_user.id
    query = update.callback_query
    # Create keyboard
    keyboard = [
        [
            InlineKeyboardButton(lang["audio.1"], callback_data='1'),
            InlineKeyboardButton(lang["audio.2"], callback_data='2'),
        ], [
            InlineKeyboardButton(lang["audio.3"], callback_data='3'),
            InlineKeyboardButton(lang["audio.4"], callback_data='4'),
        ], [
            InlineKeyboardButton(lang["audio.5"], callback_data='5'),
            InlineKeyboardButton(lang["audio.6"], callback_data='6'),
        ], [
            InlineKeyboardButton(lang["audio.7"], callback_data='7'),
            InlineKeyboardButton(lang["audio.8"], callback_data='8'),
        ], [
            InlineKeyboardButton(lang["audio.9"], callback_data='9'),
        ], [
            InlineKeyboardButton(lang["audio.1.1"], callback_data='1.1')
        ]]

    # Send keyboard
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        update.message.reply_text(
            lang["audio.audio_guide"], reply_markup=reply_markup)
    except AttributeError:
        query.edit_message_text(lang["audio.audio_guide"])
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))


def audio_submenu(update, context):
    # Init query
    query = update.callback_query
    query.answer()

    # Answers - Sources
    if str(query.data) == str("1"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.10"], callback_data='10')],
            [InlineKeyboardButton(lang["audio.11"], callback_data='11')],
            [InlineKeyboardButton(lang["audio.12"], callback_data='12')],
            [InlineKeyboardButton(lang["audio.13"], callback_data='13')],
            [InlineKeyboardButton(lang["audio.14"], callback_data='14')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Record Player
    elif str(query.data) == str("10"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.15"], callback_data='15')],
            [InlineKeyboardButton(lang["audio.16"], callback_data='16')],
            [InlineKeyboardButton(lang["audio.17"], callback_data='17')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Players
    elif str(query.data) == str("11"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.18"], callback_data='18')],
            [InlineKeyboardButton(lang["audio.19"], callback_data='19')],
            [InlineKeyboardButton(lang["audio.20"], callback_data='20')],
            [InlineKeyboardButton(lang["audio.21"], callback_data='21')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Conversion Units
    elif str(query.data) == str("2"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.22"], callback_data='22')],
            [InlineKeyboardButton(lang["audio.23"], callback_data='23')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Interfaces
    elif str(query.data) == str("3"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.24"], callback_data='24')],
            [InlineKeyboardButton(lang["audio.25"], callback_data='25')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Amplifiers
    elif str(query.data) == str("4"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.26"], callback_data='26')],
            [InlineKeyboardButton(lang["audio.27"], callback_data='27')],
            [InlineKeyboardButton(lang["audio.36"], callback_data='36')],
            [InlineKeyboardButton(lang["audio.28"], callback_data='28')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Integrated
    elif str(query.data) == str("26"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.29"], callback_data='29')],
            [InlineKeyboardButton(lang["audio.30"], callback_data='30')],
            [InlineKeyboardButton(lang["audio.31"], callback_data='31')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Analogue (A & AB Class)
    elif str(query.data) == str("30"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.32"], callback_data='32')],
            [InlineKeyboardButton(lang["audio.33"], callback_data='33')],
            [InlineKeyboardButton(lang["audio.34"], callback_data='34')],
            [InlineKeyboardButton(lang["audio.35"], callback_data='35')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Preamps
    elif str(query.data) == str("36"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.37"], callback_data='37')],
            [InlineKeyboardButton(lang["audio.38"], callback_data='38')],
            [InlineKeyboardButton(lang["audio.39"], callback_data='39')],
            [InlineKeyboardButton(lang["audio.40"], callback_data='40')],
            [InlineKeyboardButton(lang["audio.41"], callback_data='41')],
            [InlineKeyboardButton(lang["audio.42"], callback_data='42')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Audio Processing
    elif str(query.data) == str("5"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.43"], callback_data='43')],
            [InlineKeyboardButton(lang["audio.44"], callback_data='44')],
            [InlineKeyboardButton(lang["audio.45"], callback_data='45')],
            [InlineKeyboardButton(lang["audio.46"], callback_data='46')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Equalizers
    elif str(query.data) == str("45"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.47"], callback_data='47')],
            [InlineKeyboardButton(lang["audio.48"], callback_data='48')],
            [InlineKeyboardButton(lang["audio.49"], callback_data='49')],
            [InlineKeyboardButton(lang["audio.50"], callback_data='50')],
            [InlineKeyboardButton(lang["audio.51"], callback_data='51')],
            [InlineKeyboardButton(lang["audio.52"], callback_data='52')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Graphic Equalizers
    elif str(query.data) == str("48"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.53"], callback_data='53')],
            [InlineKeyboardButton(lang["audio.54"], callback_data='54')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-parametric Equalizers
    elif str(query.data) == str("50"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.55"], callback_data='55')],
            [InlineKeyboardButton(lang["audio.56"], callback_data='56')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Parametric Equalizers
    elif str(query.data) == str("51"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.57"], callback_data='57')],
            [InlineKeyboardButton(lang["audio.58"], callback_data='58')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Speakers
    elif str(query.data) == str("6"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.59"], callback_data='59')],
            [InlineKeyboardButton(lang["audio.60"], callback_data='60')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Passive
    elif str(query.data) == str("59"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.61"], callback_data='61')],
            [InlineKeyboardButton(lang["audio.62"], callback_data='62')],
            [InlineKeyboardButton(lang["audio.63"], callback_data='63')],
            [InlineKeyboardButton(lang["audio.64"], callback_data='64')],
            [InlineKeyboardButton(lang["audio.65"], callback_data='65')],
            [InlineKeyboardButton(lang["audio.66"], callback_data='66')],
            [InlineKeyboardButton(lang["audio.67"], callback_data='67')],
            [InlineKeyboardButton(lang["audio.68"], callback_data='68')],
            [InlineKeyboardButton(lang["audio.69"], callback_data='69')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Active
    elif str(query.data) == str("60"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.70"], callback_data='70')],
            [InlineKeyboardButton(lang["audio.71"], callback_data='71')],
            [InlineKeyboardButton(lang["audio.72"], callback_data='72')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Headphones
    elif str(query.data) == str("7"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.73"], callback_data='73')],
            [InlineKeyboardButton(lang["audio.74"], callback_data='74')],
            [InlineKeyboardButton(lang["audio.75"], callback_data='75')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - On-ear
    elif str(query.data) == str("73"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.76"], callback_data='76')],
            [InlineKeyboardButton(lang["audio.77"], callback_data='77')],
            [InlineKeyboardButton(lang["audio.78"], callback_data='78')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Open-back(On-ear)
    elif str(query.data) == str("76"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.79"], callback_data='79')],
            [InlineKeyboardButton(lang["audio.80"], callback_data='80')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-open-back(On-ear)
    elif str(query.data) == str("77"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.81"], callback_data='81')],
            [InlineKeyboardButton(lang["audio.82"], callback_data='82')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Closed-back(On-ear)
    elif str(query.data) == str("78"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.83"], callback_data='83')],
            [InlineKeyboardButton(lang["audio.84"], callback_data='84')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Over-ear
    elif str(query.data) == str("74"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.85"], callback_data='85')],
            [InlineKeyboardButton(lang["audio.86"], callback_data='86')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Open(Over-ear)
    elif str(query.data) == str("85"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.87"], callback_data='87')],
            [InlineKeyboardButton(lang["audio.88"], callback_data='88')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Closed(Over-ear)
    elif str(query.data) == str("86"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.89"], callback_data='89')],
            [InlineKeyboardButton(lang["audio.90"], callback_data='90')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - In-ear
    elif str(query.data) == str("75"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.91"], callback_data='91')],
            [InlineKeyboardButton(lang["audio.92"], callback_data='92')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Production Tools
    elif str(query.data) == str("8"):
        keyboard = [
            [
                InlineKeyboardButton(lang["audio.94"], callback_data='94'),
                InlineKeyboardButton(lang["audio.95"], callback_data='95'),
            ], [
                InlineKeyboardButton(lang["audio.96"], callback_data='96'),
            ], [
                InlineKeyboardButton(lang["audio.97"], callback_data='97'),
            ], [
                InlineKeyboardButton(lang["audio.98"], callback_data='98'),
                InlineKeyboardButton(lang["audio.99"], callback_data='99'),
            ], [
                InlineKeyboardButton(lang["audio.100"], callback_data='100'),
            ], [
                InlineKeyboardButton(lang["audio.101"], callback_data='101'),
            ], [
                InlineKeyboardButton(lang["audio.102"], callback_data='102'),
                InlineKeyboardButton(lang["audio.103"], callback_data='103'),
            ], [
                InlineKeyboardButton(lang["audio.104"], callback_data='104'),
                InlineKeyboardButton(lang["audio.105"], callback_data='105'),
            ], [
                InlineKeyboardButton(lang["audio.106"], callback_data='106'),
                InlineKeyboardButton(lang["audio.108"], callback_data='108'),
            ], [
                InlineKeyboardButton(lang["audio.109"], callback_data='109'),
            ], [
                InlineKeyboardButton(lang["audio.110"], callback_data='110'),
            ], [

                InlineKeyboardButton(lang["audio.0"], callback_data='0')
            ]]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Equalizers
    elif str(query.data) == str("104"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.111"], callback_data='111')],
            [InlineKeyboardButton(lang["audio.112"], callback_data='112')],
            [InlineKeyboardButton(lang["audio.113"], callback_data='113')],
            [InlineKeyboardButton(lang["audio.114"], callback_data='114')],
            [InlineKeyboardButton(lang["audio.115"], callback_data='115')],
            [InlineKeyboardButton(lang["audio.116"], callback_data='116')],
            [InlineKeyboardButton(lang["audio.117"], callback_data='117')],
            [InlineKeyboardButton(lang["audio.118"], callback_data='118')],
            [InlineKeyboardButton(lang["audio.119"], callback_data='119')],
            [InlineKeyboardButton(lang["audio.120"], callback_data='120')],
            [InlineKeyboardButton(lang["audio.121"], callback_data='121')],

            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Graphic Equalizers
    elif str(query.data) == str("113"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.122"], callback_data='122')],
            [InlineKeyboardButton(lang["audio.123"], callback_data='123')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Semi-parametric Equalizers
    elif str(query.data) == str("115"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.124"], callback_data='124')],
            [InlineKeyboardButton(lang["audio.125"], callback_data='125')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Parametric Equalizers
    elif str(query.data) == str("116"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.126"], callback_data='126')],
            [InlineKeyboardButton(lang["audio.127"], callback_data='127')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Answers - Accessories
    elif str(query.data) == str("9"):
        keyboard = [
            [InlineKeyboardButton(lang["audio.128"], callback_data='128')],
            [InlineKeyboardButton(lang["audio.129"], callback_data='129')],
            [InlineKeyboardButton(lang["audio.130"], callback_data='130')],
            [InlineKeyboardButton(lang["audio.131"], callback_data='131')],
            [InlineKeyboardButton(lang["audio.132"], callback_data='132')],
            [InlineKeyboardButton(lang["audio.0"], callback_data='0')]
        ]
        query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(keyboard))

    # Go back to to main menu
    elif str(query.data) == str("0"):
        init(update, context)
