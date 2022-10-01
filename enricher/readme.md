# Enricher

## Назначение

Сервис, который "обогащает" сырое сообщение данными из других сервисов (Auth, UGC)

## Как работает

У сервиса есть единственный эндпоинт - `/api/v1/notification/{notification_id}?type=transactional`.
где notification_id = сквозное id из монго,
а тип type - тип сообщения, принимающий 2 значения - transactional/scheduled.

Сервис ожидает сообщение вида (пример):
```json
{
  "receivers_list": [
    "user_id_1",
    "user_id_2"
  ],
  "sender": "alabama@yandex.ru",
  "event_type": "birthday",
  "transport": "sms",
  "priority": "low_priority", # low_priority/high_priority
  "created_dt": "21-06-2022 21:34:06.000+0300",
  "schedule": "0 0 * * *",
  "start_date": "27-06-2022 21:34:06.000+0300",
  "payload": {
    "header": "С днем рождения, {{first_name}} {{last_name}}!",
    "template": "template_name",
    "body": {
       "user_ids": ["user_id_1", "user_id_2"]
    }
  }
}
```

1) При запросе со стороны сервиса генератора данный сервис запрашивает из монго шаблоны для упомянутого транспорта по
   маске:

```json
{
  "name": 'template_name',
  "transport": "email"
} # sms/push/email
```

2) Далее сервис запрашивает информацию (из сервиса генератора фейковых данных) по получателям из списка receivers_list.
3) После этого сервис запрашивает данные для payload, а именно данные о пользователях, упомянутых в искомом сообщении,
   и фильмах, если таковые имеются.
4) После получения всей информации все данные рендерятся в шаблоне, полученной в п.1
5) Возвращается итоговое сообщение вида:
```json
{
  "priority": "low_priority", # low_priority/high_priority
  "type": "transactional",
  "transport": {
    "sms": [
      {
        "number": "687-740-9655",
        "message": "Привет, Андрей!"
      }
    ]
  }
}
```

Важно! Надо убедиться, что в монго хранятся шаблоны для ожидаемых типов сообщения.
Для примера это может быть что-то вроде:
```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def add_doc():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db_name = client['TEMPLATES'] # бд в монго, которая указана в конфигурационном файле
    collection = db_name["TEMPLATES"] # коллекция, которая указана в конфигурационном файле
    doc = {'name': 'birthday', 'transport': 'sms', 'body': 'Congratulations, {{first_name}} {{last_name}}!'}
    result = await collection.insert_one(doc)
    print('result %s' % repr(result.inserted_id))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_doc())
```