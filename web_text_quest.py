from flask import Flask, request, render_template_string

app = Flask(__name__)

# Хранилище состояния квеста
session_state = {}

# Отладочный вывод для логов
import os
print(f"Server starting on PORT: {os.getenv('PORT', 'not set')}")
import os
print(f"PATH: {os.getenv('PATH')}")
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        choice = request.form.get('choice')
        user_id = request.remote_addr

        if user_id not in session_state:
            session_state[user_id] = {"step": 1, "inventory": []}

        state = session_state[user_id]

        if state["step"] == 1:
            return render_template_string("""
                <h1>Текст-квест: Приключение начинается</h1>
                <p>Вы очнулись в тёмном лесу. Перед вами два пути: идти направо или налево.</p>
                <form method="post">
                    <button name="choice" value="right">Направо</button>
                    <button name="choice" value="left">Налево</button>
                </form>
            """)

        elif state["step"] == 2:
            if choice == "right":
                state["step"] = 3
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Вы нашли старый сундук! В нём меч. Взять меч?</p>
                    <form method="post">
                        <button name="choice" value="take">Взять меч</button>
                        <button name="choice" value="leave">Оставить</button>
                    </form>
                """)
            else:
                state["step"] = 4
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Вы упали в яму. Игра окончена. <a href="/">Начать заново</a></p>
                """)

        elif state["step"] == 3:
            if choice == "take":
                state["inventory"].append("меч")
                state["step"] = 5
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Вы взяли меч. Теперь вы видите выход из леса. Уйти?</p>
                    <form method="post">
                        <button name="choice" value="exit">Уйти</button>
                        <button name="choice" value="stay">Остаться</button>
                    </form>
                """)
            else:
                state["step"] = 5
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Вы оставили сундук. Выход из леса впереди. Уйти?</p>
                    <form method="post">
                        <button name="choice" value="exit">Уйти</button>
                        <button name="choice" value="stay">Остаться</button>
                    </form>
                """)

        elif state["step"] == 5:
            if choice == "exit":
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Поздравляем! Вы выбрались из леса. Ваш инвентарь: {{ inventory }}. <a href="/">Начать заново</a></p>
                """, inventory=", ".join(state["inventory"]))
            else:
                return render_template_string("""
                    <h1>Текст-квест</h1>
                    <p>Вы остались в лесу. Игра окончена. <a href="/">Начать заново</a></p>
                """)

    return render_template_string("""
        <h1>Текст-квест</h1>
        <p>Добро пожаловать! Нажмите кнопку, чтобы начать.</p>
        <form method="post">
            <button name="choice" value="start">Начать</button>
        </form>
    """)

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
