# Публикация комиксов xckd в VK
Скрипт умеет публиковать случайные [комиксы xckd](https://xkcd.com/) в группе в VK.

## Приступаем к работе
Для запуска кода у вас уже должен быть установлен Python3.
Используйте в консоли `pip` для установки зависимостей или `pip3`, если есть конфликт с Python2:
```
pip install -r requirements.txt
```
 
Затем вам необходимо создать группу в VK, куда будут публиковаться комиксы и получить её id.
Создать сообщество можно перейдя в [Сообщества](https://vk.com/groups?tab=admin).
А после этого нужно создать приложение в VK через которое будет происходить обращение к API VK (в типе приложения указываем «standalone») - [страница с приложениями](https://vk.com/apps?act=manage).

### Получаем ключи доступа
1. В первую очередь нужно узнать client_id приложения, которое вы уже создали по ссылкам выше. Для того, чтобы получить id нужно перейти на [страницу с приложениями](https://vk.com/apps?act=manage), и если нажать на кнопку «Редактировать» для нового приложения, в адресной строке вы увидите его client_id. Либо его можно посмотреть в настройках приложения.
1. Затем нужно получить ключ API. Для этого в адресную строку браузера необходимо ввести ссылку, предварительно указав в ней client_id, который вы получили ранее: 

`https://oauth.vk.com/authorize?client_id=[*здесь ваш client_id*]&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.131`.

Далее вы должны увидеть аналогичную страницу:
![comics_devman](https://user-images.githubusercontent.com/42252541/148439319-5bba535f-63b7-443c-b9d4-a6a7df90835d.png)

### Переменные окружения
Чувствительные данные, такие как токены, хранятся в переменных окружения. Для того, чтобы у вас всё работало необходимо создать файл .env в папке, где лежат скрипты. Через переменные окружения регулируются такие настройки как:
1. Ключ API VK - название переменной VK_ACCESS_TOKEN.
1. ID созданной вами группы в VK - название переменной VK_GROUP_ID.

Пример заполненного файла .env:
```
VK_CLIENT_ID='Ваш ID группы'
VK_ACCESS_TOKEN='Ваш токен для работы с API VK'
```

### Структура файлов

#### fetch_xkcd_comics.py
В данном файле содержатся функции для работы с [API xkcd](https://xkcd.com/json.html).

#### file_handler.py
Вспомогательный файл, где хранятся функции для скачивания комиксов и работы с именами файлов.

#### get_comics.py
Основной файл в котором выстроена логика по скачиванию комиксов, их публикации и последующего удаления скаченных файлов.
Чтобы запустить скрипт нужно выполнить команду в терминале:
```python get_comics.py```

По умолчанию скрипт ничего не выводит в консоль, но результат успешного выполнения вы увидите по опубликованному комиксу :)


