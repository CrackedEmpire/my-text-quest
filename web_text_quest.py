from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)

# HTML-шаблон с анимацией глитча
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Текстовый квест: InSide</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #000;
            color: #fff;
        }
        .scene {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #1a1a1a;
            border-radius: 10px;
        }
        h1 {
            color: #fff;
            text-align: center;
        }
        p {
            font-size: 16px;
            line-height: 1.5;
        }
        .rules-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .rules-table td {
            padding: 10px;
            border: 1px solid #ff0000;
            color: #ff0000;
            font-weight: bold;
        }
        .glitch {
            animation: glitch 0.5s linear infinite;
            color: #ff00ff;
            position: relative;
        }
        @keyframes glitch {
            2%, 64% {
                transform: translate(2px, 0) skew(0deg);
            }
            4%, 60% {
                transform: translate(-2px, 0) skew(0deg);
            }
            62% {
                transform: translate(0, 0) skew(5deg);
            }
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            background-color: #222;
            border-radius: 5px;
        }
        form {
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin: 5px;
            background-color: #333;
            color: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <div class="scene">
        <h1>Текстовый квест: InSide</h1>
        <p>{{ scene_text | replace('\n', '<br>') | safe }}</p>
        {% if rules %}
            <table class="rules-table">
                {% for rule in rules %}
                    <tr><td>{{ rule }}</td></tr>
                {% endfor %}
            </table>
        {% endif %}
        {% if messages %}
            {% for msg in messages %}
                <div class="message">{{ msg }}</div>
            {% endfor %}
        {% endif %}
        <form method="POST">
            {% for choice in choices %}
                <button type="submit" name="choice" value="{{ loop.index }}" {% if choice == 'Выйти на улицу' %}class="glitch"{% endif %}>{{ choice }}</button>
            {% endfor %}
        </form>
    </div>
</body>
</html>
"""

def save_progress(state):
    with open("quest_save.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False)

def load_progress():
    if os.path.exists("quest_save.json"):
        with open("quest_save.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"scene": 1, "dialog_step": 0, "choice_a": False}

@app.route("/", methods=["GET", "POST"])
def game():
    state = load_progress()
    scene = state["scene"]
    dialog_step = state["dialog_step"]
    choice_a = state["choice_a"]
    scene_text = ""
    choices = []
    rules = []
    messages = []

    if request.method == "POST":
        choice = int(request.form.get("choice", 0))

        if scene == 1 and choice:
            state["scene"] = 2
            save_progress(state)
        elif scene == 2 and choice:
            if choice == 1:  # Выглядеть в окно
                state["scene"] = 3
            elif choice == 2:  # Выйти на улицу
                state["scene"] = 4
            elif choice == 3:  # Посмотреть сообщение
                state["scene"] = 5
                state["dialog_step"] = 1
            save_progress(state)
        elif scene == 5 and choice:
            if dialog_step == 1:
                if choice == 1:  # Вариант А
                    state["choice_a"] = True
                    state["dialog_step"] = 2
                else:  # Вариант Б
                    state["choice_a"] = False
                    state["dialog_step"] = 3
                save_progress(state)
            elif dialog_step in [2, 3]:
                state["dialog_step"] = 4
                save_progress(state)
            elif dialog_step == 4 and choice:
                if os.path.exists("quest_save.json"):
                    os.remove("quest_save.json")  # Удаление сохранения
                state["scene"] = 1  # Явный возврат на главную сцену
                state["dialog_step"] = 0
                state["choice_a"] = False
                save_progress(state)

    # Определение текущей сцены
    if state["scene"] == 1:
        scene_text = """
        2025.07.22  
        Этот день нам запомнился надолго. До этого всё было не сказать, что так ужасно. Привычные дни жары, ничего не предвещающие новости... Уже тогда нас должно было насторожить изменение погоды. Ничего, в сущности, необычного. Только разве что бабочки исчезли. А вместе с ними и стрекозы. Не помню, когда в последний раз эти крылатые создания появлялись на глаза. Это был первый и очень явный знак, который мы все проигнорировали. Зря.  
        Трубили о том, что исчезли пчёлы. Ну, об этом уж говорили все и на каждом шагу. Все охали и ахали, сокрушаясь о гибели прелестных полосатых созданий, но дальше дело не пошло. Исчезли и исчезли - вечно, что ли, слёзы лить?  
        Это было только начало. Мы должны были это понять.  
        После началась чехарда с погодой. Не просто то солнце, то дождь. Нет, торнадо могло возникнуть из ниоткуда, а буквально через секунду светило солнце или шёл дождь. Летом солнце испепеляло людей так сильно, что выход на улицу стал опасен. И даже тогда мы не перестали считать это обычными капризами погоды.  
        Нам было дано последнее предупреждение.  
        Потом произошло ЭТО. Целый континент раскололся на две части. Нет смысла объяснять, какой урон это нанесло цивилизации. Новости, репортажи всё про это и всё ни о чём. Беда не обошла стороной никого. Следующее землетрясение уничтожило несколько стран.  
        Вот тогда все всполошились.  
        Но было уже поздно.  
        Мы попытались спастись. Как крысы с тонущего корабля, у которого всюду дыры и пробоины. Просто другого корабля у человечества не было. Тут-то мы осознали всю плачевность нашего положения. Когда невозможно выйти на улицу днём, когда воды не хватает, когда животные исчезают, а вместе с ними исчезаем и мы.  
        Планета избавлялась от паразитов. Это ли не иронично?  
        Правительства были озабочены скорее собственным выживанием, но в том и был парадокс. Если спасутся только они, золотой миллиард, кто будет работать, кто будет их обслуживать?  
        Тогда-то и началась суматоха номер два.  
        Довольно банально, даже я это понимаю, но правительство предложило выход. Проект назывался «InSide», и он защищал людей, но для реализации этой защиты нам было нужно выполнять несколько правил.
        """
        rules = [
            "1. Не выходите на улицу после 00:00",
            "2. Избегайте тёмных узких переулков.",
            "3. Если с вами заговорит незнакомый человек с искаженными, неправильными чертами лица - бегите.",
            "4. Если ваше животное избегает или боится определенного места - немедленно покиньте это место.",
            "5. Не включайте ТВ и радио после 00:00.",
            "6. Не смотрите в зеркало после 00:00.",
            "7. Если вы слышите, как вас зовёт чей-то голос, но вы не знаете, откуда он доносится, игнорируйте его.",
            "8. Если ваш друг/родственник ведёт себя странно, игнорируйте его.",
            "9. Если хотя бы одно из этих правил будет нарушено, ваша жизнь окажется в опасности. Вы можете позвонить в Министерство Безопасности и сообщить о нарушении протокола «InSide».",
            "10. Помните: ваша безопасность зависит только от вас!"
        ]
        choices = ["Принять правила и продолжить"]

    elif state["scene"] == 2:
        scene_text = """
        Сегодня вечером вам было тревожно. За окном шёл дождь, и вы не могли понять, кажется вам, что там кто-то ходит или это ваше разыгравшееся воображение. В любом случае, кажется, вы просто слишком устали после работы.  
        Телефон под рукой завибрировал. Вы вздрогнули. Слишком резкий звук, а вы так привыкли к тишине и звуку дождя...
        """
        choices = ["Выглядеть в окно", "Выйти на улицу", "Посмотреть сообщение"]

    elif state["scene"] == 3:
        scene_text = """
        Вы подошли к окну и заглянули наружу. Тень оказалась человеком с искажённым лицом. Он заметил вас и начал приближаться!  
        Вы в опасности. Квест окончен.  
        Нажмите любую кнопку, чтобы начать заново.
        """
        choices = ["Начать заново"]

    elif state["scene"] == 4:
        scene_text = """
        Вы вышли на улицу. Внезапно мир вокруг начал искажаться, и вы почувствовали, как реальность рушится. Это было последнее, что вы видели.  
        Вы нарушили правило. Квест окончен.  
        Нажмите любую кнопку, чтобы начать заново.
        """
        choices = ["Начать заново"]

    elif state["scene"] == 5:
        if dialog_step == 0:
            scene_text = """
            Вы посмотрели на загоревшийся экран телефона. Имя было вам знакомо - Уильям, ваш друг. Вы знали друг друга так давно, что, кажется, время и обстоятельства были не властны над вами.
            """
            messages = ["Уильям: Хэй, Марго... Как ты? В последнее время ты звучишь так измучено."]
            choices = ["А) Всё в порядке. Просто мигрени.", "Б) Я ощущаю, что за мной кто-то следит..."]
        elif dialog_step == 1:
            if choice_a:
                messages = ["Уильям: Понимаю. Погодные условия :Р"]
                choices = ["Ха-ха, очень смешно, гений."]
            else:
                messages = ["Уильям: Ты уже сообщала на работе, так?"]
                choices = ["Не могу. Ты же знаешь. Министерство не...Ладно, забей."]
        elif dialog_step == 2 or dialog_step == 3:
            messages = ["Уильям: (если вариант Б, продолжение) Чтобы в один прекрасный момент ты исчезла? Нет, спасибо."]
            choices = ["Ха-ха, очень смешно, гений."]
        elif dialog_step == 4:
            scene_text = """
            Разговор с Уильямом немного вас отвлёк, но за окном снова послышались шаги. Кажется, пора принимать решение.  
            Квест окончен.  
            Нажмите любую кнопку, чтобы начать заново.
            """
            choices = ["Начать заново"]

    return render_template_string(HTML_TEMPLATE, scene_text=scene_text, choices=choices, rules=rules, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)