# Всё для настройки (надеюсь ничего не забыл)


## 1. Клонируем репозиторий

Сначала нужно склонировать репозиторий на свой локальный компьютер. Для этого выполни следующую команду в терминале:

```bash
git clone "ссылка"
```

## 2. Настраиваем окружение
### 2.1. Создаем виртуальное окружение

Войди в каталог проекта и создайте виртуальное окружение с помощью следующей команды:

```bash
python -m venv venv
```
Активируй виртуальное окружение:

```bash
venv\Scripts\activate
```

Затем установи зависимости проекта, используя команду:

```bash
pip install -r requirements.txt
```
### 2.2. Создаем файл .env

В корневом каталоге проекта создай файл .env и добавь туда все необходимые переменные окружения, такие как пароли, ключи для доступа к базе данных и другие конфиденциальные данные. Пример содержимого файла .env может выглядеть так:

```env

DB_HOST=localhost
DB_PORT=5432
DB_USER=yourusername
DB_PASSWORD=yourpassword
SECRET_KEY=your_secret_key
``` 

Убедись, что файл .env включен в .gitignore, чтобы не подвергать конфиденциальные данные риску.

## 3. Проверь API на работоспособность 

Пропиши (будь внимательней откуда запускаешь приложение):

```bash
uvicorn src.main:app --reload 
```

## 4. Для поднятия сервисов баз для локальной разработки нужно запустить команду:

```bash
make up
```

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```bash
alembic init migrations
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

В `alembic.ini` нужно задать адрес базы данных, в которую будем катать миграции.
Дальше идём в папку с миграциями и открываем `env.py`, там вносим изменения в блок, где написано `from myapp import mymodel`
Дальше вводим: `alembic revision --autogenerate -m "comment"` - делается при любых изменениях моделей
Будет создана миграция
Дальше вводим: `alembic upgrade heads`