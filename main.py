from telebot import TeleBot, types

bot = TeleBot("")

# Глобальный словарь для ответов пользователя
user_answers = {}

# Типы деятельности и их соответствующие вопросы
types_answers = {
    "Работа с природой": ["1а", "3б", "6а", "10а", "11а", "13б", "16а", "20а"],
    "Работа с технологиями": ["1б", "4а", "7б", "9а", "11б", "14а", "17б", "19а"],
    "Работа с людьми": ["2а", "4б", "6б", "8а", "12а", "14б", "16б", "18а"],
    "Аналитическая работа": ["2б", "5а", "9б", "10б", "12б", "15а", "19б", "20б"],
    "Творческая деятельность": ["3а", "5б", "7а", "8б", "13а", "15б", "17а", "18б"]
}

# Вопросы теста
questions = {
    1: ["Ухаживать за животными", "Обслуживать машины, приборы (следить, регулировать)"],
    2: ["Помогать больным", "Составлять таблицы, схемы, программы для вычислительных машин"],
    3: ["Следить за качеством книжных иллюстраций, плакатов", "Следить за состоянием, развитием растений"],
    4: ["Обрабатывать материалы (дерево, металл и т.п.)", "Доводить товары до потребителя, рекламировать, продавать"],
    5: ["Обсуждать научно-популярные книги, статьи", "Обсуждать художественные книги (или пьесы, концерты)"],
    6: ["Выращивать молодняк (животных какой-либо породы)", "Тренировать товарищей (или младших) в выполнении каких-либо действий (трудовых, учебных, спортивных)"],
    7: ["Копировать рисунки, изображения (или настраивать музыкальные инструменты)", "Управлять каким-либо грузовым (подъемным или транспортным) средством – подъемным краном, трактором, тепловозом и др."],
    8: ["Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.)", "Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов)"],
    9: ["Ремонтировать вещи, изделия (одежду, технику), жилище", "Искать и исправлять ошибки в текстах, таблицах, рисунках"],
    10: ["Лечить животных", "Выполнять вычисления, расчеты"],
    11: ["Выводить новые сорта растений", "Конструировать, проектировать новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.)"],
    12: ["Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять", "Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок)"],
    13: ["Наблюдать, изучать работу кружков художественной самодеятельности", "Наблюдать, изучать жизнь микробов"],
    14: ["Обслуживать, налаживать медицинские приборы, аппараты", "Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п."],
    15: ["Художественно описывать, изображать события (наблюдаемые и представляемые)", "Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др."],
    16: ["Делать лабораторные анализы в больнице", "Принимать, осматривать больных, беседовать с ними, назначать лечение"],
    17: ["Красить или расписывать стены помещений, поверхность изделий", "Осуществлять монтаж или сборку машин, приборов"],
    18: ["Организовать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п.", "Играть на сцене, принимать участие в концертах"],
    19: ["Изготавливать по чертежам детали, изделия (машины, одежду), строить здания", "Заниматься черчением, копировать чертежи, карты"],
    20: ["Вести борьбу с болезнями растений, с вредителями леса, сада", "Работать на клавишных машинах (пишущей машинке, телетайпе, наборной машине и др.)"],
}
# Упрощенная логика создания клавиатуры
def create_keyboard(options):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in options:
        markup.add(option)
    return markup

# Обработка ответа и переход к следующему вопросу
def process_answer(message, question_number):
    user_input = message.text.strip().lower()
    current_options = questions[question_number]
    options_lower = [opt.lower() for opt in current_options]

    if user_input not in options_lower:
        bot.send_message(message.chat.id, "Пожалуйста, выберите один из предложенных вариантов.")
        bot.register_next_step_handler(message, lambda m: process_answer(m, question_number))
        return

    answer_letter = "а" if options_lower.index(user_input) == 0 else "б"
    user_answers[f"{question_number}{answer_letter}"] = message.text

    # Если есть следующий вопрос
    if question_number + 1 in questions:
        ask_question(message, question_number + 1)
    else:
        finish_test(message)

# Задаем вопрос
def ask_question(message, question_number):
    options = questions[question_number]
    bot.send_message(
        message.chat.id,
        f"Вопрос {question_number}: {options[0]} или {options[1]}?",
        reply_markup=create_keyboard(options)
    )
    bot.register_next_step_handler(message, lambda m: process_answer(m, question_number))

# Финализация теста
def finish_test(message):
    scores = {key: 0 for key in types_answers}
    for answer in user_answers.keys():
        for category, answers in types_answers.items():
            if answer in answers:
                scores[category] += 1

    max_category = max(scores, key=scores.get)
    # Очистка данных
    user_answers.clear()
    match max_category:
        case "Работа с природой":
            bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Сельское, лесное и рыбное хозяйство
            - Экология, природообустройство и безопасность
            ''')
            bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
            start(message)

        case "Работа с технологиями":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add("Техническое направление", "Химико-техническое")
            bot.send_message(message.chat.id, "Выберите одно из двух наиболее привлекательных направлений:", reply_markup=markup)
        case "Работа с людьми":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add("Социально-химическое", "Лингвистическое", "Социально-техническое", "Социальное направление")
            bot.send_message(message.chat.id, "Выберите одно из четырёх наиболее привлекательных направлений:", reply_markup=markup)
        case "Аналитическая работа":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add("Аналитическо-лингвистическое", "Аналитическо-техническое")
            bot.send_message(message.chat.id, "Выберите одно из двух наиболее привлекательных направлений:", reply_markup=markup)
        case "Творческая деятельность":
            bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Искусство, культура, дизайн
            ''')
            bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
            start(message)
@bot.message_handler(func=lambda message: message.text == "Техническое направление")
def show_1(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Математика, информационные науки и технологии
            - Машинотроение, автоматизация и робототехника
            - Транспорт
            - Строительство, архитектура и недвижимость
            - Электроника, связь и радиотехника
            - Энергетика и электротехника
            - Физико-технические науки и технологии
            - Качество и управление в технических системах
            - Технологии легкой и пищевой промышленности
            - Приборостроение, оптика и биотехника
            - Технологии машины, оборудование и спецтранспорт
            - Оружие и системы вооружения
            - Технологии материалов и металлургия
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Химико-техническое")
def show_2(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Нанотехнологии и наноматериалы
            - Химико-биологические науки и технологии
            - Науки о земле, геология и геодезия
            - Технологии легкой и пищевой промышленности
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Социально-химическое")
def show_3(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Медицина и здравоохранение
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Лингвистическое")
def show_4(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Филология и лингвистика
            - Юриспруденция
            - Политика и международные отношения
            - Философия и религия
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Социально-техническое")
def show_5(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Качество и управление в технических системах
            - Торговля и товароведение
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Социальное направление")
def show_6(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Управление и менеджмент
            - Образование и педагогика
            - Сервис, туризм и гостиничное дело
            - СМИ, журналистика, реклама и PR
            - Психология
            - Физическая культура, спорт и фитнес
            - Политика и международные отношения
            - Социология и социальная работа
            - Управление персоналом
            - Маркетинг
            - Философия и религия
            - Торговля и товароведение
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Аналитическо-лингвистическое")
def show_7(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Юриспруденция
            - Филология и лингвистика
            - История, археология и документирование
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)
@bot.message_handler(func=lambda message: message.text == "Аналитическо-техническое")
def show_8(message):
    bot.send_message(message.chat.id,
            '''
            Ваши направления для дальнейшей учебы или работы:
            - Математика, информационные науки и технологии
            - Экономика и финансы
            - Транспорт
            - Науки о земле, геология и геодезия
            - Логистика
            ''')
    bot.send_message(message.chat.id, "Здесь Вы можете подобрать ВУЗы для себя \n https://spb.postupi.online/")
    start(message)


# Стартовый обработчик
@bot.message_handler(commands=["start"])
def start(message):
    user_answers.clear()
    bot.send_message(
        message.chat.id,
        "Привет! Я чат-бот, который поможет подобрать наиболее подходящую профессию для тебя.",
        reply_markup=create_keyboard(["Написать профориентационный тест"])
    )

@bot.message_handler(func=lambda message: message.text == "Написать профориентационный тест")
def start_test(message):
    ask_question(message, 1)

if __name__ == "__main__":
    bot.polling(non_stop=True)
