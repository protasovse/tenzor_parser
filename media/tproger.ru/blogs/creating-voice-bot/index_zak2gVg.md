Создание голосового бота: взаимодействие с веб-интерфейсом через мобильный телефон
==================================================================================

*Рассказывает Василий Корянов,*  
 *frontend-разработчик облачной коммуникационной платформы Voximplant*

Этой осенью мне довелось собрать бота, который одновременно общается с пользователем голосом и показывает картинки в браузере. Оказалось, что это не так просто, поэтому я решил поделиться пошаговым руководством, демками и исходниками нашего робота. Его, кстати, зовут Павел, и он виртуальный рептилоид, который разыгрывал билеты на конференцию INTERCOM’18.

### Почему не просто голосовой бот

Сделать обычного голосового робота было бы быстрее, но я не мог не реализовать мечту детства — повторить опыт создания легендарной игры девяностых «Позвоните Кузе». Если вы не помните, двадцать лет назад на канале РТР по утрам шла интерактивная передача, куда могли дозвонится дети со всей страны. После соединения телефон «становился» джойстиком, с помощью которого можно было управлять персонажем, наблюдая за процессом по ТВ.

![](https://cdn.tproger.ru/wp-content/plugins/a3-lazy-load/assets/images/lazy_placeholder.gif)

![](https://cdn.tproger.ru/wp-content/uploads/2018/12/Illjustracija-1-e1545144952367.jpg)Тогда это казалось мне магией. Сейчас я занимаюсь разработкой и понимаю, что для девяностых это и правда была магия: взаимодействие с интерфейсом игры с помощью телефона, да ещё и стриминг на всю страну. Итак, «Позвоните Кузе» — это отличный пример нетривиального пути взаимодействия с интерфейсом, который мы взяли за основу при создании своего бота.

### Что умеет Павел

![](https://cdn.tproger.ru/wp-content/plugins/a3-lazy-load/assets/images/lazy_placeholder.gif)

![](https://cdn.tproger.ru/wp-content/uploads/2018/12/Illjustracija-3.jpg)С 1 сентября по 11 октября Павел «жил» во всплывающем окне на сайте конференции и предлагал каждому посетителю сыграть с ним. Пользователь оставлял свой номер телефона, звонил на бесплатный номер Павлу, и сессия браузера синхронизировалась со звонком. Далее участник должен был голосом давать ответы на ребусы, которые видел на экране. Робот распознавал речь, а потом дарил скидку в зависимости от количества правильных ответов.

При этом, если указанный номер уже поучаствовал в розыгрыше, рептилоид выдавал ошибку: «Одна попытка в одни руки — таковы правила».

Можно [посмотреть](https://youtu.be/8gkAomN-jNM), как это работало, или пообщаться лично с Павлом, который специально для Tproger переехал на [отдельную страницу](https://grindpride.github.io/pavel.html). Кстати, из порядка 150 участников, сыгравших с нашим роботом, ни один не смог с первой попытки ответить верно на все вопросы. Но не стоит отчаиваться, многие позвонившие всё же справились с большей частью ребусов.

### Как синхронизировать браузер и телефон

Есть несколько путей узнать, кто именно из пользователей, находящихся в данный момент на сайте, сейчас будет общаться с ботом:

* **Авторизация**. Если сайт предполагает авторизацию по номеру, синхронизировать сессию браузера с телефоном можно непосредственно в момент звонка.
* **Уникальные номера**. Можно закупить номера и предлагать каждому пользователю свой — это удобно, но слишком дорого.
* **Пароль**. Идентификатором может стать уникальный текст, который пользователь проговорит в начале звонка — бот распознает речь и свяжет сценарий с браузером.
* **Уникальное действие на странице**. И наоборот — пользователь может ввести в окне на сайте пин-код, который ему назовёт бот.
* **Ввод телефонного номера на странице**. В этом случае в качестве идентификатора используется сам номер — так мы и сделали.
![](https://cdn.tproger.ru/wp-content/plugins/a3-lazy-load/assets/images/lazy_placeholder.gif)

![](https://cdn.tproger.ru/wp-content/uploads/2018/12/Illjustracija-4-e1545144824985.jpg)Разберем подробнее, как это работает. Пользователь вводит номер, браузер отправляет запрос на бэкенд в http, бэкенд устанавливает Socket-сессию. Далее участник звонит на многоканальный номер, обозначенный на сайте. В облаке Voximplant запускается сценарий, который также отправляет запрос в бэкенд — есть ли сейчас зарегистрированная Socket-сессия с определенным идентификатором. Если нет — звонок прерывается, если же да — начинается игра.

### Как устроен сценарий

Участник общается с ботом голосом: сценарий звонка отправляет http-запросы бэкенду, а бэкенд через Socket-сессию взаимодействует с пользователем. Так, бэкенд может показать картинку, вывести ответ пользователя на экран и, если участник выиграл, сообщить промокод.

![](https://cdn.tproger.ru/wp-content/plugins/a3-lazy-load/assets/images/lazy_placeholder.gif)

![](https://cdn.tproger.ru/wp-content/uploads/2018/12/Illjustracija-5.jpg)### Методы и код Павла

**Событийная модель**. Поскольку Voximplant использует JavaScript, у которого есть событийная модель, сценарий подключается прямо к телефонному номеру, и любой сценарий начинается с подписки на событие самого звонка. Именно в callback этого события мы пишем логику звонка: что говорить, как реагировать, записывать или не записывать звонок.

VoxEngine.addEventListener(AppEvents.CallAlerting,e => { //some logic } **call.say() для синтеза**. Чтобы робот говорил, используется метод call.say(), он принимает строку, которую нужно проговорить, и тип голоса, которым бот будет общаться с пользователем — наш Павел может говорить и женским, и мужским голосом. А вообще есть библиотека голосов, которые можно подобрать для своего бота.

call.say("Привет, давай поиграем", Language.RU\_RUSSIAN\_MALE)**Модуль Net для связи с внешним миром**. Сценарий может связываться с бэкендом через модуль Net, который шлёт http-запросы (а они отлично парсятся).

Net.httpRequest() Net.httpRequestAsync() **VoxEngine.createASR для распознавания**. Чтобы бот понимал, что говорит пользователь, и переводил речь в текст, используется модуль распознавания ASR. Здесь очень важно указать язык, который вы собираетесь распознавать.

VoxEngine.createASR({ lang: ASRLanguage.RUSSIAN\_RU, }) **Cheat: Помогаем роботу распознавать речь**. Распознавание не всегда работает идеально, но есть выход — «скормить» машине словарь из ожидаемых слов. В этом случае нейросеть сначала пройдётся по заданному словарю и, если не найдёт совпадений, определит слово самостоятельно. В нашем случае было очень удобно загрузить правильные ответы.

VoxEngine.createASR({ lang: ASRLanguage.RUSSIAN\_RU, dict: ['Мозила фаирфокс', 'мазила', 'фаирфокс'] }) ### Sharing is caring

Чтобы окончательно разобраться в принципе работы Павла, предлагаю самостоятельно покопаться в его [исходниках](https://github.com/irbisadm/panda-pavel). Можно развернуть рептилоида на своём устройстве или посмотреть сохраненные сценарии звонка и серверный скрипт, чтобы понять принцип написания подобного голосового бота. Там всё просто — немного Express.js и в продакшн.


> **Подобрали два теста для вас:**  
>  — [А здесь можно применить блокчейн?](https://tprg.ru/UcBz)  
>  — [Серверы для котиков: выберите лучшее решение для проекта и проверьте себя.](https://tprg.ru/8S2a)
> 
>  * [Боты](https://tproger.ru/tag/bots/)
#### 

* <>
* <>
* <>
* <>
* <>
* <>
* <>
 