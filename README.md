LinkedIn Parser

## Опис проєкту

Цей проєкт — парсер для LinkedIn, розроблений на Python із використанням Selenium. Він автоматизує вхід у профіль LinkedIn та парсинг потрібних даних.

#### Основні можливості:
- Авторизація в LinkedIn (через логін та пароль).
- Парсинг даних із LinkedIn.
- Логування процесу у локальну директорію logs.
- Запуск у Docker-контейнері для спрощення розгортання та уникнення проблем із залежностями.

## Передумови
- Встановлений Docker та Docker Compose
- Python 3.10+ (якщо запускати без Docker).


### Конфігурація .env
Внести в файл .env логін та пароль від LinkedIn:
```
LINKEDIN_LOGIN=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## Запуск проєкту

### Linux / macOS
Збірка Docker-образу:
```
sudo docker build --no-cache -t linkedin-parser .
```

Запуск Docker-контейнера:
```
sudo docker run --rm -it --name linkedin-parser-container -v \$(pwd)/logs:/app/logs linkedin-parser
```

### Windows (через PowerShell)
Збірка Docker-образу:
```
docker build --no-cache -t linkedin-parser .
```

Запуск Docker-контейнера:
```
docker run --rm -it --name linkedin-parser-container -v ${PWD}/logs:/app/logs 
linkedin-parser
```

### Альтернатива: Запуск без Docker

Створи віртуальне середовище та активуй його:
```
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate    # Windows
```

Встанови залежності:
```
pip install -r requirements.txt
```

Запусти парсер:
```
python main.py
```

### Логування
Усі логи зберігаються в директорії logs/.
Якщо запускаєш через Docker, ця директорія монтується автоматично.