# Fake data generator
## Назначение
Генератор событий для уведомлений, предназначенных Notification Event API.
Построен на основе FastAPI+Faker.
Умеет отсылать уведомления и возвращать фейковые запросы по user и movie.
Отсылает уведомления по расписанию, заданному в REPEAT_TASK_EVERY_SECONDS
