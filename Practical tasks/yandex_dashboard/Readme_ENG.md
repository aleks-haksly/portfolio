# Yandex Queries Overview

## Install

To install, you first need to load the dataset.zip data into PostgreSQL according to the column descriptions in Section 1.
The application can be run in a Docker container. You need to specify the connection string in the environment variable:
```bash
docker build -t yandex_dashboard:1 -e dbconnect=<YOUR_CONNECTION STRING> .
```

## 1. Data Source

This project analyzes search query data from Yandex for the period 2021-09-01 to 2021-09-21, comprising 1.2M records stored in a CSV file.

### Dataset Fields:
- `ts` : Date and time of the query.
- `query` : Search query text.
- `platform`  ("desktop", "touch"): User platform.

To facilitate data processing:
- All query text was converted to lowercase, and the character `ё` was replaced with `е`.
- The data was uploaded to a PostgreSQL database hosted on [Supabase](https://supabase.com/).

Two main database objects were created:
1. **Table `yandex_data`**: Contains raw data fields (`ts`, `platform`, `query`).
2. **Materialized View `yandex_data_agg`**: Aggregated data by hours, days, weeks, and platforms with fields:
   - `ts`, `scale`, `platform`, `count`.
```sql
  CREATE MATERIALIZED VIEW vizro.yandex_data_agg as
SELECT
    date_trunc('h', ts) AS ds, 
    'hours' AS scale,
    platform,
    count(*) AS count
FROM vizro.yandex_data yd 
GROUP BY date_trunc('h', ts), platform

UNION 

SELECT
    date_trunc('d', ts) AS ds, 
    'days' AS scale,
    platform,
    count(*) AS count
FROM vizro.yandex_data yd 
GROUP BY date_trunc('d', ts), platform

UNION 

SELECT
    date_trunc('week', ts) AS ds, 
    'weeks' AS scale,
    platform,
    count(*) AS count
FROM vizro.yandex_data yd 
GROUP BY date_trunc('week', ts), platform

ORDER BY ds;
  
  ```


### Indexing:
B-tree indexes were created for each column to optimize query performance. However, this provided only marginal improvements given the specific usage patterns of the dataset.

## 2. Dashboard Structure

The dashboard consists of three pages:

### 1. (Overview Dashboard)
![Overview_dashboard](img/Overview_dashboard.jpg)
The primary page provides a quantitative overview of query dynamics over time:

- Time slices:
  - Hourly
  - Daily
  - Weekly
- Platform-wise breakdown.

#### Key Features:

- **Date Range Selector:** Allows filtering by specific date ranges. A monthly view is omitted due to the limited 3-week dataset.
- **Pie Chart:** Displays the proportion of queries by platform. Approximately 75% of queries were made from mobile devices (platform: `touch`).
- **Line Chart:** Shows query dynamics by platform for the selected date range, with hourly granularity.
- **Anomaly Detection:**
  - A predictive model using [Prophet](https://facebook.github.io/prophet/) was employed to detect anomalies.
  - Model quality:
    - MAE: 80
    - MAPE: 20.55%
  - Values outside the 95% confidence interval are flagged as anomalies.
- **Trend Components:** Separate graphs for overall, weekly, and daily trends are included to visualize seasonal patterns.

### 2. (Queries Counts Detailed)
![Queries Counts Detailed](img/Queries_counts_detailed.jpg)

This page provides detailed insights into query counts:

- **Heatmaps:**
  - Display query counts by hour for each day over the last 7 days.
  - Show week-over-week differences in absolute and percentage terms.
  - Highlight clear intra-week and daily patterns, distinct for each platform.
  
- **Date Range Selector:** Allows filtering by specific date ranges. 

### 3. (Queries Text Detailed)
![Queries Text Detailed](img/Queries_text_detailed.jpg)
This page focuses on the textual analysis of popular queries:

#### Key Features:

1. **Butterfly Chart:**

   - Displays the top 10 most popular queries for both platforms.
   - Compares query shares as a percentage of total queries for each platform.
   - Example:
     - The query "обои на рабочий стол" accounts for 0.26% of desktop queries but only 0.01% of mobile queries, reflecting logical platform-specific behavior.

2. **Line Charts:**

   - Show hourly dynamics for the top 5 most popular queries on each platform.
   - Highlight trends aligned with typical user activity patterns (e.g., work and rest cycles).
   - Note: Potential noise arises from the absence of user-specific timezone data.

3. **Data Table:**

   - Contains query counts and shares for the selected time range, broken down by platform.
   - Includes a `p-value` column, calculated using the chi-squared test, to determine the statistical significance of differences in query shares:
     - Green cells (`p-value < 5%`) indicate significant differences, suggesting platform-specific preferences.
     - Cells without green highlights indicate no significant difference in query frequency between platforms.

- **Date Range Selector:** Allows filtering by specific date ranges. 
- **Filter min sum query counts:** to display on dashboard
---

This dashboard provides an in-depth analysis of search queries, uncovering key patterns and trends across platforms and time. The inclusion of anomaly detection and statistical testing ensures robust and actionable insights.
