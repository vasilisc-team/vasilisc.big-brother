
# vasilisc.budget

**Стек технологий [основной]**

Python         |  Django   | Docker  | Pandas   | Sklearn   | TensorFlow | NymPy |
:------------------------:|:------------------------:|:----------------------:|:----------------------:|:----------------------:|:----------------------:|:----------------------:|
<img src=https://e.sfu-kras.ru/pluginfile.php/1794713/course/overviewfiles/%D0%9B%D0%BE%D0%B3%D0%BE%D1%82%D0%B8%D0%BF.jpg width="64" height="64" />|<img src=https://to-moore.com/images/django.png width="64" height="64" />|<img src=https://www.kubeclusters.com/img/index/docker-logo.png width="64" height="64" />|<img src=https://jehyunlee.github.io/thumbnails/Python-DS/1-pandas1.png width=64 height=64/>|<img src=https://pythondatalab.files.wordpress.com/2015/04/skl-logo.jpg width=64 height=64/>|<img src=https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/TensorFlowLogo.svg/1200px-TensorFlowLogo.svg.png width="64" height="64" />|<img src=https://user-images.githubusercontent.com/82882128/132093816-429d9b14-941f-4c52-adfa-4bc9ac426a03.png width="64" height="64" />| 


[![github workflow CI img]][github workflow CI]

[github workflow CI img]: https://github.com/xausssr/vasilisc.budget/actions/workflows/build-ci.yaml/badge.svg
[github workflow CI]: https://github.com/xausssr/vasilisc.budget/actions/workflows/build-ci.yaml

Сервис представляет собой веб-приложение, упрощающее работу аналитика и позволяющее планировать региональный бюджет на основе различных моделей анализа, в том числе, искусственных нейронных сетей. Аналитик может посмотреть дашборд с представлением наиболее влиятельных метрик, сводной статистики и прогнозом, автоматически созданным системой, а также загрузить данные о бюджете за предыдущие периоды для просмотра нового прогноза. 


Уникальность: возможность загрузки данных напрямую в модель и их автоматический анализ, построение отдельных моделей планирования для наиболее значимых параметров, прогнозирвоание консолидирвоанного бюджета на основе ARIMA, исторических данных, предсказаний предыдущего шага, предсказание бюджета на основе ИНС, выдача сводной статистики.

# Demo
[Сайт](https://vasilisc.ru:59443/)

# Аналитика

Директория Research содержит Jupyter Notebook с моделями
Исследование представляет из себя:

- анализ вклада в бюджет различных статей (наименьший/наибольший вклад, топ прибыльных/убыточных статей)
- анализ корелляции и корелляционную матрицу признаков
- построение базовой модели для анализа и прогнозирвоания временных рядов ARIMA
- построение отдельных моделей планирования для наиболее значимых параметров
- выдача метрик по отдельным полям
- прогнозирвоание консолидирвоанного бюджета на основе ARIMA, исторических данных, предсказаний предыдущего шага
- обучение искусственной нейронной сети и предсказание бюджета на основе ИНС
- выдача сводной статистики
- верификация на другом наборе данных: Федеральный бюджет за 2016-2020 г.г.

Для запуска jupyter-тетрадки необходимы следующие зависимости `>= python.3.7`:
- `pandas` : 1.1.3
- `numpy` : 1.20.1
- `statsmodels` : 0.12.2
- `sklearn` : 0.23.0
- `tensorflow` : 2.2.0


# Среда запуска
Необходим Docker.

# Установка веб-сервера
Данный репозиторий имеет настроеный ci/cd пайплайн, автоматически собирающий актуальный docker-контейнер. 

Установка:

`$ docker pull ghcr.io/xausssr/vasilisc.budget:latest`

**Установка вне docker не рекомендуется!**

# Команда
Толстых Андрей &minus; analitics, ML [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/tolstykhaa)

Ельчугин Максим &minus; fullstack, CI/CD  [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/pariah_max)

Суворов Арнольд &minus; analitics, ML [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/SSHINRATENSSEI)

Маямсин Сергей &minus; backend [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/Sinserelyyy)

Гаус Глеб &minus; disign, UX/UI [<img src=https://pbs.twimg.com/media/ErZeb4AXYAAuKFm.jpg width="15" height="15" />](https://t.me/grey_landlord)
