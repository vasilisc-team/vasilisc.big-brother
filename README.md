# vasilisc.big-brother

**Стек технологий [основной]**

Python         |  Django   | Docker  | Pandas   | Sklearn   | TensorFlow | NymPy |
:------------------------:|:------------------------:|:----------------------:|:----------------------:|:----------------------:|:----------------------:|:----------------------:|
<img src=https://e.sfu-kras.ru/pluginfile.php/1794713/course/overviewfiles/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF.jpg width="64" height="64" />|<img src=https://to-moore.com/images/django.png width="64" height="64" />|<img src=https://www.kubeclusters.com/img/index/docker-logo.png width="64" height="64" />|<img src=https://jehyunlee.github.io/thumbnails/Python-DS/1-pandas1.png width=64 height=64/>|<img src=https://pythondatalab.files.wordpress.com/2015/04/skl-logo.jpg width=64 height=64/>|<img src=https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/TensorFlowLogo.svg/1200px-TensorFlowLogo.svg.png width="64" height="64" />|<img src=https://user-images.githubusercontent.com/82882128/132093816-429d9b14-941f-4c52-adfa-4bc9ac426a03.png width="64" height="64" />|


[![github workflow CI img]][github workflow CI]

[github workflow CI img]: https://github.com/vasilisc-team/vasilisc.big-brother/actions/workflows/build-ci.yaml/badge.svg
[github workflow CI]: https://github.com/vasilisc-team/vasilisc.big-brother/actions/workflows/build-ci.yaml

Данный репозиторий представляет собой набор моделей и вариантов их использования для интеграции с "безопасным городом". В директории research находятся соответсвующие jupyter-тетрадки с конвеерами (пайплайнами) моделей и оценкой результатов. Предусмотрен telegram-бот для сбора разметки от населения. Приведен пример реализации предложенных моделей в форме web-приложения (демо) на основе docker-контейнера.

Уникальность:
* построены детектор (mAP на один класс [мусорные контейнеры] **~ 0.4**) и классификатор (AUC бинарной классификации переполненности контейнера **0.98**)
* построена линейная модель выделения неработающих элементов уличного освещения
* реализован сервис выделения и улучшения качества (апскеил $\times 2$) изображений лиц из полученных кадров
* реализована классическая модель детектирования (YOLOv3) для выявления собак на кадрах
* реализована модель распознавания движений (позы человека) для дальнейшего распознавания действий

# Demo
[Сайт](https://vasilisc.ru:58443/)

![Детектор мусора](trash_detector.gif)

# Аналитика

Директория Research содержит Jupyter Notebook'и с моделями:

* RubbishNet
  * анализ датасета
  * выделение изображений по заданным bbox'ам
  * аугментация полученных обучающих образцов
  * обучение классификатора и его валидация
* RubbishDetector
  * дообучение детектора на основе SSD-архитектуры
  * валидация детектора
* lights
  * анализ возможности автоматического выделения осветительных приборов (фонарей)
  * ручная разметка
  * анализ линейной разделимости рабочих и не рабочих фонарей в ночное время

----------
# Планируем до СТОП_КОДИНГА:

# Docker контейнер

# Telegram-бот

----------
# Команда
Толстых Андрей &minus; analitics, ML [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/tolstykhaa)

Ельчугин Максим &minus; fullstack, CI/CD  [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/pariah_max)

Суворов Арнольд &minus; analitics, ML [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/SSHINRATENSSEI)

Маямсин Сергей &minus; backend [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/Sinserelyyy)

Гаус Глеб &minus; disign, UX/UI [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/grey_landlord)
