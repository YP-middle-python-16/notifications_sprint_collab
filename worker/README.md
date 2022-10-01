# Worker

## Назначение
Воркер следит за сообщениями в rabbitmq и производит рассылку по email, sms или push.
Результат обработки сообщения возвращает Notification Event API.

Пример сообщения в брокере
```json
{
    "notification_id": "str",
    "priority": "hight",
    "type": "transactional",
    "transport": {
        "email": {
            "address": "apenshin@gmail.com",
            "message": "1",
            "subject": "Тестовое письмо"
        }
   }
}
```
Статус рассылки отправляется на /api/v1/event/status