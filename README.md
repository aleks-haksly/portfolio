# Portfolio
Portfolio Analyst CV

## Marketing analytics
---
1. Сегментируем клиентов с помощью RFM анализа и определяем стратегии взаимодействия (`pandas/seaborn`) [здесь...](/Marketing%20analytics/RFM/RFM%20analysis.ipynb)
2. Проведем многомерный ABC совмещенный с XYZ анализом товаров, продаваемых в аптечной сети (`pandas/sqlalchemy/window_functions`) [здесь...](/Marketing%20analytics/ABC/ABC.ipynb)
3. Считаем Retention, Lifetime, Churn, MAU/WAU/DAU (`pandas/seaborn`) [здесь...](/Marketing%20analytics/Metrics/Metrics.ipynb)
4. Считаем юнит экономику по когортам: ARRPPU, LTV, [COGS, CAC] (`clickhouse/pandas/seaborn`) [здесь...](/Marketing%20analytics//UNIT/unit_economics.ipynb)
   

## Small projects
---
1. Строим предсказательные модели и запускаем [сайт](https://kagglerecsys.streamlit.app/)-дашборд на [датасете](https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system/data?select=movies.csv) Kaggle о просмотре фильмов (sklearn/LR/XGBR/aiohttp/streamlit) [Здесь...](https://github.com/aleks-haksly/Streamlit/blob/main/README.md) 
2. Парсим данные об экономических показателях деятельности компаний с сайта **nalog.ru** и изучаем перспективы строительной отрасли путем анализа изменения показателя [EBITDA](https://национальныепроекты.рф/news/chto-takoe-ebitda/) российских компаний за последние 4 года (`pandas/requests/seaborn/geopandas`) [здесь...](/Practical%20tasks/nalog.ru/EBITDA%20analysis.ipynb)
3. Верстаем и поднимаем в докере дашборд о поисковых запросах Яндекса. Забираем данные из [postgres](https://supabase.com/), детектим аномалии и тренды во временном ряде с помощью fb Prophet. (PostgreSQL/Vizro/Plotly/Prophet/Dash/Docker) [здесь..](/Practical%20tasks/yandex_dashboard)
4. Строим Overview дашборд в Tableau для команды листинга платформы объялений [здесь..](https://public.tableau.com/views/HardDAv10table/ListingsOverview?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
## SQL
---
1. Базовый SQL (`pandas/sqlalchemy/postgresql/joins/window_functions`) [здесь...](/SQL/simple/sql_simple.ipynb)
2. Оптимизируем размер на диске таблицы ClickHouse (`pandas/codecs/partitions/clickhouse_driver`) [здесь...](/SQL/optimization/ClickHouse_table_size_optimization.ipynb)
