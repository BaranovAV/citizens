## Common

This project was created for Yandex backend school. Author suggests that server will be installed in path `/var/www/citizen`.

You need to create mysql database, create `settings.py` and `yoyo.ini` files from default ones and apply all migrations using `yoyo`.

These operations must be automated later with fabric or smth else.

## Start project
### Simple way 

Use `python server.py` to start server directly in your CLI. Server listens to `0.0.0.0` address with `8080` port.

### Better way (not best)
 
We can just order system to run app as a service:

1. `cd /lib/systemd/system`
2. `sudo touch citizen.service`. Content of `citizen.service`:<br/><br/>
[Unit]<br/>
Description=Very Important Service<br/>
Requires=mysql.service<br/><br/>
[Service]<br/>
Type=idle<br/>
ExecStart=/var/www/citizens/venv/bin/python /var/www/citizens/server.py<br/>
Restart=always<br/>
TimeoutStartSec=1<br/><br/>
[Install]<br/>
WantedBy=multi-user.target<br/><br/>
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable citizen.service`
5. `sudo systemctl start citizen.service`
6. `sudo systemctl status citizen.service`

## Testing

Use `py.test -c tests/pytest.ini` command to run all tests in project.

## Migrations

Use `yoyo apply` to apply new available migrations.

## Extra

You can generate big massive of good test data to make "load" testing. Use `python tests/generate_data.py`

## PS

Процесс разворачивания приложения по сути не реализован - хотел использовать для этого fabric, но эта утилита пока в процессе изучения. Хотел с помощью нее генерить конфиги (однако при таком подходе не понимаю, где хранить логины/пароли от БД и других сервисов), накатывать новые миграции (возможно даже тестировать, но это уже забегание в тему CI).

Так же не очень удачной по мне оказалась идея использовать `systemd` для запуска приложения как сервиса - в таком случае не очень понятно, что делать, если нужно запустить несколько инстансов, так же логи работы приложения в текущей реализации посмотреть негде (а хотелось бы, но это все же можно было настроить). Так же при обновлении кода сервер надо перезапускать, а значит, для пользователя он "мигнет", лучше прятать приложение за `nginx`-ом, самому следить за его "поднятостью" и реализовать сине-зеленый деплой для плавного переключения, но этого я пока не умею:) 

Тестирование так же не идеально - с pytest уже некоторое время работаю, но ввиду специфики своего проекта удавалось писать только нечто похожее на интеграционное тестирование, написал как умею.