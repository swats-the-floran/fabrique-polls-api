admin_login: admin\
admin_password: admin

installation:\
$ git clone https://github.com/swats-the-floran/fabrique-polls-api \
$ cd fabrique-polls-api/\
$ python -m venv venv\
$ source venv/bin/activate\
(venv)$ export SECRET_KEY=some_key_you_generated\
(venv)$ pip install -r requirements.txt\
(venv)$ python manage.py migrate

launch:\
(venv)$ python manage.py runserver

swagger documentation is at http://127.0.0.1:8000/swagger and http://127.0.0.1:8000/swagger.json

Из задания не до конца реализована только последняя функция с возвратом всех опросов с вложенными ответами по пользовательскому id.\
Тем не менее полнота данных обеспечена, потому что модель ответа привязана не только к вопросу, но и к самому опросу через ForeignKey.

Разделение моделей оции вопроса и ответа на вопрос, возможно, является перереусложнением. Логика такова, что опция ответа будет недобросовестно изменена, то предыдущие ответы станут невалидными, потому что перестанут совпадать с опцией ответа на вопрос.\
В следствие такой архитектуры реализованы некоторые дополнительные валидаторы. Например при ответе на вопрос с типом radio_answer или check_answer происходит проверка соответствия опциям этого вопроса.
