# 🦄 REST сервис для хранения дат дней рождений друзей

Добро пожаловать в проект, который реализует REST сервис для хранения дат дней рождений. Этот сервис позволяет пользователям создавать, редактировать и удалять данные дате дня рождения друзей и об их пожеланиях в выборе подарка.

## Установка

Для использования этого сервиса необходимо склонировать репозиторий на свой компьютер и установить все необходимые зависимости. Используйте следующие команды для установки:

```
git clone https://github.com/MariaSvintsova/real_exam.git
cd real_exam
sudo docker build -t masha .

```

## 🚀 About Me
I'm a skypro course student. I'm going to be Junior Python developer. 


## Запуск

Для запуска сервиса выполните следующую команду:

```
sudo docker run -p 80:80 -d masha
```

## Использование

После запуска, вы можете использовать API сервиса для создания, редактирования и удаления заметок пользователей. Для этого отправляйте HTTP запросы с помощью любой программы или скрипта, который умеет делать HTTP запросы.

Описание доступных методов:



### Получение дней рождений всех ваших друзей

`GET /birthday/`

### Создание ДР

`POST /birthday`

Создает новый ДР и возвращает созданный объект. Необходимо передать JSON объект в теле запроса со следующими свойствами:

* `fio` - ФИО друга
* `date` - дата рождения
* `wish` - пожелания в выборе подарка.

### Получение дня рождения по идентификатору друга

```http
  GET /birthday/<friend_id>
```

| Parameter   | Type     | Description       |
|:------------| :------- |:------------------|
| `friend_id` | `string` | **birthday note** |

Возвращает объект заметки с указанным идентификатором `noteId`.

### Обновление дня рождения

`PUT /birthday/<friend_id>`

| Parameter   | Type     | Description       |
|:------------| :------- |:------------------|
| `friend_id` | `string` | **birthday note** |

Обновляет существующий день рождения с указанным идентификатором `friend_id`. Необходимо передать JSON объект в теле запроса со следующими свойствами:

* `fio` - ФИО друга
* `date` - дата рождения
* `wish` - пожелания в выборе подарка.



### Удаление дня рождения

`DELETE /birthday/<friend_id>`

| Parameter   | Type     | Description               |
|:------------| :------- |:--------------------------|
| `friend_id` | `string` | **deleted birthday note** |


Удаляет день рождения с указанным идентификатором `friend_id`.

## 🔗 Links  
How to reach me: [![TG Badge](https://img.shields.io/badge/Svintsova_Maria-blue?style=flat&logo=telegram&logoColor=white)](https://t.me/mariyapy)