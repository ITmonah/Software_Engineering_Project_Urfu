from datetime import datetime


def log(function_name: str, comment: str, level: str = "INFO") -> None:
    # Печатает в консоль время, уровень, имя функции и короткое сообщение в колонках
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    time_col = now  # ширина 19
    level_col = level.upper()
    func_col = function_name
    msg_col = comment

    level_width = 7
    func_width = 30

    level_formatted = level_col.center(level_width)
    func_formatted = func_col.ljust(func_width)

    if level_col == "ERROR":
        level_colored = f"\033[97;41m{level_formatted}\033[0m"
    elif level_col == "INFO":
        level_colored = f"\033[97;44m{level_formatted}\033[0m"
    else:
        level_colored = level_formatted

    line = f"{time_col} | {level_colored} | {func_formatted} | {msg_col}"
    print(line)
