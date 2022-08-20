from telegram import *
from telegram.ext import *
import datetime as dt
from dateutil.relativedelta import relativedelta
import requests
from database import user
from configs import Config

print("start")
answer = 9999
fullname = ""
membership = 0
startmembership = 00-00-0000
endmembership = 00-00-0000
iduser = 000000000
chat_admin1 = "646510124"
chat_admin2=Config.ADMIN_ID
offer = ""
# chatid_spot=-1001743888874
# chatid_future=-1001790260583
chatid_spot="-100"+Config.SPOT_ID
chatid_future="-100"+Config.FUTURE_ID
token = Config.BOT_TOKEN

def send_msg(text):
   url="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(chat_admin2)+"&parse_mode=Markdown&text="
   request = url+text
   requests.get(request)

def banmembers(chat_id, user_id):
   url="https://api.telegram.org/bot"+str(token)+"/banChatMember?chat_id="+str(chat_id)+"&user_id="+str(user_id)
   request = url
   requests.get(request)

def start(update, context):
    try:
        if str(update.message.chat_id) == chat_admin1 or str(update.message.chat_id) == chat_admin2:
            keyboard = [[KeyboardButton("👤 إضافة عضو جديد "), KeyboardButton("👥 قائمة المشتركين ")], [KeyboardButton("⚙️ تعديل بيانات المشتركين")], [KeyboardButton("🗑 حذف المشتركين")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            update.message.reply_text('*👋 مرحبا بك عزيزي الأدمن  *`'+update.effective_user.full_name+'`*\n\nيمكنك الإختيار من القائمة الموجودة في الأسفل 👇*', parse_mode="Markdown", reply_markup=reply_markup)
        else:
            members = user.allmembers(collection = "members", Owenr=chat_admin2)
            liste = []
            for i in members[0]:
                liste.append(i["iduser"])
            if str(update.message.chat_id) not in liste:
                msg = "🆔*:* `"+str(update.message.chat_id)+"`\n\n*👤 Full Name: *`"+update.effective_user.full_name+"`"
                send_msg(msg)
                update.message.reply_text('*👋 مرحبا بك عزيزي  *`'+update.effective_user.full_name+'`*\n\nبعد أن يقوم الأدمن بإضافتك فالبوت ستتوصل هنا برابط الإنضمام للقناة👇*', parse_mode="Markdown")
    except :
        pass

def handlmsg(update, context):
    if str(update.message.chat_id) == chat_admin1 or str(update.message.chat_id) == chat_admin2:
        global answer, fullname, membership, startmembership, endmembership, iduser, offer

        if update.message.text == "⛔️ إلغاء":
            try:
                keyboard = [[KeyboardButton("👤 إضافة عضو جديد "), KeyboardButton("👥 قائمة المشتركين ")], [KeyboardButton("⚙️ تعديل بيانات المشتركين")], [KeyboardButton("🗑 حذف المشتركين")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text('*👋 مرحبا بك عزيزي الأدمن  *`'+update.effective_user.full_name+'`*\n\nيمكنك الإختيار من القائمة الموجودة في الأسفل 👇*', parse_mode="Markdown", reply_markup=reply_markup)
                answer = 9999
            except:
                answer = 9999
                pass

        if update.message.text == "👤 إضافة عضو جديد":
            try:
                keyboard = [[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✏️ أدخل الإسم الكامل للعضو *", parse_mode="Markdown", reply_markup=reply_markup)
                answer = 0
            except:
                answer = 9999
                pass

        if update.message.text == "📋 العودة للقائمة الرئيسية":
            try:
                keyboard = [[KeyboardButton("👤 إضافة عضو جديد "), KeyboardButton("👥 قائمة المشتركين ")], [KeyboardButton("⚙️ تعديل بيانات المشتركين")], [KeyboardButton("🗑 حذف المشتركين")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text('*👋 مرحبا بك عزيزي الأدمن  *`'+update.effective_user.full_name+'`*\n\nيمكنك الإختيار من القائمة الموجودة في الأسفل 👇*', parse_mode="Markdown", reply_markup=reply_markup)
                answer = 9999
            except:
                answer = 9999
                pass

        if update.message.text == "👥 قائمة المشتركين":
            try:
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                if int(members[1])>0:
                    for mb in members[0]:
                        fullname = mb["fullname"]
                        membership= mb["membership"]
                        startmembership = mb["startmembership"]
                        endmembership = mb["endmembership"]
                        endmembership = mb["endmembership"]
                        iduser = mb["iduser"]
                        if mb["spot"] == "true" and mb["future"] == "false":
                            offer = "سبوت"
                        elif mb["spot"] == "false" and mb["future"] == "true":
                            offer = "فيوتشر"
                        else:
                            offer = "سبوت و فيوتشر"

                        update.message.reply_text("*👤   الإسم الكامل: *`"+str(fullname)+"`\n\n*🕔 مدة الإشتراك بالأيام: *`"+str(membership)+"`\n\n*🕔 تاريخ إبتداء الإشتراك: *`"+str(startmembership)+"`\n\n*🕔 تاريخ إنتهاء عضويته: *`"+str(endmembership)+"`\n\n*🆔: *`"+str(iduser)+"`*\n\n📊 نوع الإشتراك: *`"+offer+"`", parse_mode="Markdown", reply_markup=reply_markup)
                else:
                    update.message.reply_text("*⚠️ لم تقم بإضافة أي عضو بعد*", parse_mode="Markdown", reply_markup=reply_markup)
                    answer = 9999
            except:
                answer = 9999
                pass

        if update.message.text == "⚙️ تعديل بيانات المشتركين":
            try:
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                buttons = []
                if int(members[1])>0:
                    for mb in members[0]:
                        buttons.append([KeyboardButton(mb["fullname"])])
                    buttons.append([KeyboardButton("⛔️ إلغاء")])
                    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                    update.message.reply_text("*📃 إختر إسم العضو من القائمة أسفله*", parse_mode="Markdown", reply_markup=keyboard)
                    answer = 20

                else:
                    keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                    update.message.reply_text("*⚠️ لم تقم بإضافة أي عضو بعد*", parse_mode="Markdown", reply_markup=reply_markup)
                    answer = 9999
            except:
                answer = 9999
                pass

        if update.message.text == "✏️ تعديل تاريخ إنتهاء الإشتراك" and answer == 22:
            try:
                keyboard = [[KeyboardButton("➕ إضافة أيام للإشتراك")], [KeyboardButton("➖ نقصان أيام من للإشتراك")], [KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*📋 إختر من القائمة أسفله*", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                pass

        if update.message.text == "📊 تعديل نوع الإشتراك" and answer == 22:
            keyboard = [[KeyboardButton("📉 سبوت"), KeyboardButton("📈 فيوتشر")], [KeyboardButton("📊 سبوت و فيوتشر")], [KeyboardButton("⛔️ إلغاء")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            update.message.reply_text("*📊 إختر نوع الإشتراك *", parse_mode="Markdown", reply_markup=reply_markup)
            answer = 50

        if update.message.text == "➕ إضافة أيام للإشتراك" and answer == 23:
            try:
                keyboard = [[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*🕔 مدة الإشتراك بالأيام *\n\n `🌑 مثال: لو اشتراك شهر واحد ارسل رقم 30, لو شهرين أرسل رقم 60 وهكذا...`", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer=9999

        if update.message.text == "➖ نقصان أيام من للإشتراك"and answer == 23:
            try:
                keyboard = [[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*🕔 عدد الأيام الذي تريد نقصانه من الإشتراك*\n\n `🌑 مثال: لو تريد نقص شهر واحد ارسل رقم 30, لو شهرين أرسل رقم 60 وهكذا...`", parse_mode="Markdown", reply_markup=reply_markup)
                answer=30
            except:
                answer=9999

        if update.message.text == "🗑 حذف المشتركين":
            try:
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                buttons = []
                if int(members[1])>0:
                    for mb in members[0]:
                        buttons.append([KeyboardButton(mb["fullname"])])
                    buttons.append([KeyboardButton("⛔️ إلغاء")])
                    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
                    update.message.reply_text("*📃 إختر إسم العضو من القائمة أسفله*", parse_mode="Markdown", reply_markup=keyboard)
                    answer = 40

                else:
                    keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                    update.message.reply_text("*⚠️ لم تقم بإضافة أي عضو بعد*", parse_mode="Markdown", reply_markup=reply_markup)
                    answer = 9999
            except:
                answer = 9999
                pass
        
        if answer == 1:
            try:
                fullname = str(update.message.text).upper()
                update.message.reply_text("*🕔 مدة الإشتراك بالأيام *\n\n `🌑 مثال: لو اشتراك شهر واحد ارسل رقم 30, لو شهرين أرسل رقم 60 وهكذا...`", parse_mode="Markdown")
            except:
                answer = 0
                pass

        if answer == 2:
            try:
                membership = int(update.message.text)
                time = dt.datetime.now()
                time = time.strftime("%d-%m-%Y")
                keyboard = [[KeyboardButton(time)],[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*🕔 تاريخ إبتداء الإشتراك *\n\n `🌑 مثال: أرسل التاريخ بالشكل التالي:\n23-09-2022\n15-02-2023\n10-12-2024`", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                update.message.reply_text("*🙁 يبدو أنك أخطأت في إدخال عدد أيام الإشتراك, جرب مرة أخرى*", parse_mode="Markdown")
                answer = 1

        if answer == 3:
            try:
                startmembership = update.message.text
                startmembership = dt.datetime.strptime(startmembership,"%d-%m-%Y")
                endmembership = startmembership + relativedelta(days=membership)
                endmembership = endmembership.strftime("%d-%m-%Y")
                startmembership = startmembership.strftime("%d-%m-%Y")
                keyboard = [[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*🆔 قم بإعطاء هذا البوت للمشترك \nوطلب منه أن يضغط على *`start\n\n`*ثم ستتوصل بالأيدي الخاص به هنا, بعد ذلك قم بإرساله للبوت.*", parse_mode="Markdown", reply_markup=reply_markup)

            except:
                update.message.reply_text("*🙁 يبدو أنك أخطأت في إدخال تاريخ إبتداء الإشتراك, جرب مرة أخرى*", parse_mode="Markdown")
                answer = 2

        if answer == 4:
            try:
                iduser = update.message.text
                keyboard = [[KeyboardButton("📉 سبوت"), KeyboardButton("📈 فيوتشر")], [KeyboardButton("📊 سبوت و فيوتشر")], [KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*📊 إختر نوع العرض *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 3
        
        if answer == 5:
            try:
                offres = ["📉 سبوت", "📈 فيوتشر", "📊 سبوت و فيوتشر"]
                offer = update.message.text
                if offer in offres:
                    if offer == "📉 سبوت":
                        offer = "سبوت"
                    elif offer == "📈 فيوتشر":
                        offer = "فيوتشر"
                    else:
                        offer = "سبوت و فيوتشر"
                    keyboard = [[KeyboardButton("✅ تأكيد")],[KeyboardButton("⛔️ إلغاء")]]
                    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                    update.message.reply_text("*❓ هل أنت متأكد من أنك تريد إضافة * `"+fullname+"` *كعضو\n\n🕔 تاريخ بدء عضويته: *`"+str(startmembership)+"`*\n\n🕔 تاريخ إنتهاء عضويته: *`"+str(endmembership)+"`\n\n*🆔 الأيدي الخاص به: *`"+str(iduser)+"`*\n\n📊 نوع الإشتراك: *`"+offer+"`", parse_mode="Markdown", reply_markup=reply_markup)
                else:
                    update.message.reply_text("*📊 قم بختيار نوع العرض بناءا على العروض المتوفرة في القائمة*", parse_mode="Markdown")
                    answer = 4
            except:
                answer = 4
                pass

        if answer == 6:
            try:
                spot = ""
                future = ""
                if offer == "سبوت":
                    spot = "true"
                    future = "false"
                elif offer == "فيوتشر":
                    spot = "false"
                    future = "true"
                else:
                    spot = "true"
                    future = "true"
                user.addmembers(collection = "members", fullname = fullname.upper(), membership = str(membership), startmembership = startmembership, endmembership = endmembership, iduser = str(iduser), spot=spot, future=future, Owenr=chat_admin2)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تمت إضافة المشترك * `"+fullname+"` *بنجاح*", parse_mode="Markdown", reply_markup=reply_markup)
                bot = Bot(token=token)
                if spot == "true":
                    link = bot.createChatInviteLink(chatid_spot,  member_limit=1)
                    link = link["invite_link"]
                    msg = "🔗 رابط القناة الخاصة - سبوت 👇\n\n"+str(link)
                    bot.send_message(iduser, msg)
                if future == "true":
                    link = bot.createChatInviteLink(chatid_future,  member_limit=1)
                    link = link["invite_link"]
                    msg = "🔗 رابط القناة الخاصة - فيوتشر 👇\n\n"+str(link)
                    bot.send_message(iduser, msg)
                answer = 9999
            except:
                answer = 5
                pass

        if answer == 21:
            try:
                fullname = str(update.message.text).upper()
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                lists = []
                keyboard = [[KeyboardButton("✏️ تعديل تاريخ إنتهاء الإشتراك")], [KeyboardButton("📊 تعديل نوع الإشتراك")], [KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                for mb in members[0]:
                    lists.append(mb["fullname"])
                if fullname in lists:
                        update.message.reply_text("*📋 إختر من القائمة أسفله, الشيء الذي تريد تغييره*", parse_mode="Markdown", reply_markup=reply_markup)
                else:
                    update.message.reply_text("*🙁 يبدو أنك أدخلت إسم غير موجود في قاعدة البيانات, جرب مرة أخرى*", parse_mode="Markdown")
                    answer = 20
            except:
                answer = 9999

        if answer == 24:
            try:
                membership = int(update.message.text)
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                keyboard = [[KeyboardButton("✅ تأكيد")],[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                oldendmembership = 0
                for i in members[0]:
                    if i["fullname"] == fullname:
                        oldmembership = i["membership"]
                        oldendmembership = i["endmembership"]
                        break
                oldendmembership = dt.datetime.strptime(oldendmembership,"%d-%m-%Y")
                endmembership = oldendmembership + relativedelta(days=membership)
                endmembership = endmembership.strftime("%d-%m-%Y")
                membership = membership + int(oldmembership)
                update.message.reply_text("*🕔 تاريخ إنتهاء اللإشتراك الجديد: *`"+str(endmembership)+"`*\n\nإضغط تأكيد لتنفيذ هذه العملية*", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                update.message.reply_text("*🙁 يبدو أنك أخطأت في إدخال عدد أيام الإشتراك, جرب مرة أخرى*", parse_mode="Markdown")
                answer = 23

        if answer == 25:
            try:
                user.editmembers(collection = "members", fullname = str(fullname), membership = membership, endmembership = endmembership, Owenr=chat_admin2)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تم التعديل بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 9999
                pass

        if answer == 31:
            try:
                membership = int(update.message.text)
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                keyboard = [[KeyboardButton("✅ تأكيد")],[KeyboardButton("⛔️ إلغاء")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                oldendmembership = 0
                for i in members[0]:
                    if i["fullname"] == fullname:
                        oldmembership = i["membership"]
                        oldendmembership = i["endmembership"]
                        break
                oldendmembership = dt.datetime.strptime(oldendmembership,"%d-%m-%Y")
                endmembership = oldendmembership - relativedelta(days=membership)
                endmembership = endmembership.strftime("%d-%m-%Y")
                membership =  int(oldmembership) - membership
                update.message.reply_text("*🕔 تاريخ إنتهاء اللإشتراك الجديد: *`"+str(endmembership)+"`*\n\nإضغط تأكيد لتنفيذ هذه العملية*", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                update.message.reply_text("*🙁 يبدو أنك أخطأت في إدخال عدد الأيام الذي تريد نقصها من الإشتراك, جرب مرة أخرى*", parse_mode="Markdown")
                answer = 30

        if answer == 32:
            try:
                user.editmembers(collection = "members", fullname = str(fullname), membership = membership, endmembership = endmembership, Owenr=chat_admin2)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تم التعديل بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 9999
                pass
        
        if answer == 41:
            try:
                fullname = str(update.message.text).upper()
                members = user.allmembers(collection = "members", Owenr=chat_admin2)
                lists = []
                keyboard = [[KeyboardButton("⛔️ إلغاء"), KeyboardButton("✅ التأكيد")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                for mb in members[0]:
                    lists.append(mb["fullname"])
                    if fullname == mb["fullname"]:
                        iduser = mb["iduser"]
                        if mb["spot"] == "true" and mb["future"] == "false":
                            offer = "سبوت"
                        elif mb["spot"] == "false" and mb["future"] == "true":
                            offer = "فيوتشر"
                        else:
                            offer = "سبوت و فيوتشر"
                if fullname in lists:
                    if offer == "سبوت":
                        update.message.reply_text("*📋 هل أنت متأكد من أنك تريد حذف المشترك *`"+str(fullname)+"`* من قناة السبوت*", parse_mode="Markdown", reply_markup=reply_markup)
                        answer = 60
                    elif offer == "فيوتشر":
                        update.message.reply_text("*📋 هل أنت متأكد من أنك تريد حذف المشترك *`"+str(fullname)+"`* من قناة الفيوتشر*", parse_mode="Markdown", reply_markup=reply_markup)
                        answer = 65
                    else:
                        keyboard = [[KeyboardButton("📉 سبوت"), KeyboardButton("📈 فيوتشر")], [KeyboardButton("📊 سبوت و فيوتشر")], [KeyboardButton("⛔️ إلغاء")]]
                        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                        update.message.reply_text("*📋 إختر القناة التي تريد حذف المشترك منها *", parse_mode="Markdown", reply_markup=reply_markup)
                        answer = 70
                else:
                    update.message.reply_text("*🙁 يبدو أنك أدخلت إسم غير موجود في قاعدة البيانات, جرب مرة أخرى*", parse_mode="Markdown")
                    answer = 40
            except:
                answer = 9999
                pass

        if answer == 51:
            try:
                offres = ["📉 سبوت", "📈 فيوتشر", "📊 سبوت و فيوتشر"]
                offer = update.message.text
                if offer in offres:
                    keyboard = [[KeyboardButton("✅ تأكيد")],[KeyboardButton("⛔️ إلغاء")]]
                    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                    update.message.reply_text("*❓ هل أنت متأكد من أنك تريد تعديل نوع الإشتراك *", parse_mode="Markdown", reply_markup=reply_markup)
                else:
                    update.message.reply_text("*📊 قم بختيار نوع العرض بناءا على العروض المتوفرة في القائمة*", parse_mode="Markdown")
                    answer = 22
            except:
                answer = 22
                pass
        
        if answer == 52:
            try:
                spot = ""
                future = ""
                if offer == "📉 سبوت":
                    spot = "true"
                    future = "false"
                elif offer == "📈 فيوتشر":
                    spot = "false"
                    future = "true"
                else:
                    spot = "true"
                    future = "true"
                user.editmembers1(collection = "members", fullname = str(fullname), spot = spot, future = future, Owenr=chat_admin2)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تم التعديل بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 9999
                pass

        if answer == 61:
            try:
                user.deletemembers(collection = "members", fullname = str(fullname), Owenr=chat_admin2)
                banmembers(chatid_spot, iduser)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تم الحذف بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 9999
                pass

        if answer == 66:
            try:
                user.deletemembers(collection = "members", fullname = str(fullname), Owenr=chat_admin2)
                banmembers(chatid_future, iduser)
                keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                update.message.reply_text("*✅ تم الحذف بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
            except:
                answer = 9999
                pass
        
        if answer == 71:
            try:
                offres = ["📉 سبوت", "📈 فيوتشر", "📊 سبوت و فيوتشر"]
                offer = update.message.text
                if offer in offres:
                    if offer == "📉 سبوت":
                        user.editmembers1(collection = "members", fullname = str(fullname), spot = "false", future = "true", Owenr=chat_admin2)
                        banmembers(chatid_spot, iduser)
                        keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                        update.message.reply_text("*✅ تم الحذف بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
                    elif offer == "📈 فيوتشر":
                        user.editmembers1(collection = "members", fullname = str(fullname), spot = "true", future = "false", Owenr=chat_admin2)
                        banmembers(chatid_future, iduser)
                        keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                        update.message.reply_text("*✅ تم الحذف بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
                    else:
                        user.deletemembers(collection = "members", fullname = str(fullname), Owenr=chat_admin2)
                        banmembers(chatid_future, iduser)
                        banmembers(chatid_spot, iduser)
                        keyboard = [[KeyboardButton("📋 العودة للقائمة الرئيسية")]]
                        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                        update.message.reply_text("*✅ تم الحذف بنجاح *", parse_mode="Markdown", reply_markup=reply_markup)
                else:
                    update.message.reply_text("*📊 قم بختيار نوع العرض بناءا على العروض المتوفرة في القائمة*", parse_mode="Markdown")
                    answer = 70 
            except:
                answer = 70
                pass
        
        answer += 1

updater = Updater(token, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, handlmsg))
updater.start_polling()
updater.idle()
