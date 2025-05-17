
## 📝 Aufgabenbuch API

FastAPI-сервис для управления задачами с авторизацией по токену и фильтрацией.

---

### 📚 Описание API

**Базовый URL:** `http://localhost:8000`

| Метод    | Путь              | Описание                                            |
| -------- | ----------------- | --------------------------------------------------- |
| `POST`   | `/tasks/`         | Создать новую задачу                                |
| `GET`    | `/tasks/`         | Получить список задач (фильтрация по статусу, дате) |
| `GET`    | `/task/{task_id}` | Получить конкретную задачу по ID                    |
| `PUT`    | `/task/{task_id}` | Обновить задачу                                     |
| `DELETE` | `/task/{task_id}` | Удалить задачу                                      |

✅ Все эндпоинты защищены авторизацией с помощью Bearer Token.

---

### 🚀 Инструкции по запуску локально

1. **Клонировать репозиторий**

   ```bash
   git clone https://github.com/username/aufgabenbuch-api.git
   cd aufgabenbuch-api
   ```

2. **Создать виртуальное окружение и установить зависимости**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Создать `.env` файл**
   В файле `.env` укажи токены пользователей:

   ```
   ADMIN_TOKEN=supersecrettoken123
   ```

4. **Запустить сервер**

   ```bash
   uvicorn main:app --reload
   ```

---

### 🔍 Примеры запросов (curl / Postman)

#### 1. Создание задачи

```bash
curl -X POST http://localhost:8000/tasks/ -H "Authorization: Bearer 22222" -H "Content-Type: application/json" -d "{\"title\": \"Сдать проект\", \"description\": \"До понедельника\", \"status\": \"new\"}"
```

#### 2. Получение списка задач с фильтрацией

```bash
curl -X GET "http://localhost:8000/tasks/?status=done" -H "Authorization: Bearer supersecrettoken123"
```

#### 3. Получение одной задачи

```bash
curl -X GET http://localhost:8000/task/1 -H "Authorization: Bearer supersecrettoken123"
```

#### 4. Обновление задачи

```bash
curl -X PUT http://localhost:8000/task/1 -H "Authorization: Bearer supersecrettoken123" -H "Content-Type: application/json" -d "{\"title\": \"Обновлённый заголовок\", \"status\": \"in_progress\"}"
```

#### 5. Удаление задачи

```bash
curl -X DELETE http://localhost:8000/task/1 -H "Authorization: Bearer supersecrettoken123"
```

---

### 🤔 Рефлексия

#### ❓ Что было самым сложным в задании?

Сама работа с базой данных и нормализация логики FastAPI, так как у меня не было большого опыта с этими технологиями. Также пришлось побороть прокрастинацию, чтобы довести проект до конца.

#### ✅ Что получилось особенно хорошо?

Красивый вывод ошибок и логов в консоли 😄
(А если серьёзно — сложно выделить что-то одно, но получился рабочий API с авторизацией и фильтрацией.)

#### 🔧 Что бы вы доработали при наличии времени?

* Добавил бы алгоритмы шифрования и полноценную авторизацию.
* Реализовал бы адекватную регистрацию/добавление пользователей.
* Возможно, добавил бы простой CLI-интерфейс для локального управления задачами.

#### ⏱️ Сколько времени заняло выполнение?

В районе 10 часов.

#### 📚 Чему вы научились при выполнении?

* Работа с FastAPI, зависимостями и схемами
* Структурирование REST API с CRUD-операциями
* Использование SQLAlchemy и Pydantic
* Работа с авторизацией и проксирование пользователя через Depends
