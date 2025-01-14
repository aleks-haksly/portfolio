from vizro import Vizro
import vizro.models as vm
from vizro.tables import dash_ag_grid
from utils.helpers import (
    outliers_line_plot, components_plot, heatmap_plot, fig_kpi_date,
    fig_kpi_touch, fig_kpi_desk, fig_graph_pie, butterfly,
    linechart_query_plot
)
from utils.data_loader import read_text, data_manager, get_table_data

# Overview page
## KPI Container with multiple graphs
kpi_container = vm.Container(
    id="kpi_container",
    title="",
    components=[fig_kpi_date, fig_kpi_touch, fig_kpi_desk, fig_graph_pie],
    layout=vm.Layout(grid=[[0, 1, 2, 3]])
)

# Line Charts Tabbed Component for Outlier Detection
line_charts_tabbed = vm.Tabs(
    tabs=[
        # Touch Outlier Detection Tab
        vm.Container(
            title="Outlier Detection - Touch",
            components=[
                vm.Graph(
                    id="forecast_graph_touch",
                    figure=outliers_line_plot('forecast_touch')
                ),
                vm.Graph(
                    id="forecast_components_touch",
                    figure=components_plot('forecast_touch')
                )
            ],
            layout=vm.Layout(grid=[[0, 0, 1]])
        ),
        # Desktop Outlier Detection Tab
        vm.Container(
            title="Outlier Detection - Desktop",
            components=[
                vm.Graph(
                    id="forecast_graph_desktop",
                    figure=outliers_line_plot('forecast_desktop')
                ),
                vm.Graph(
                    id="forecast_components_desktop",
                    figure=components_plot('forecast_desktop')
                )
            ],
            layout=vm.Layout(grid=[[0, 0, 1]])
        ),
    ]
)

# Page Overview layout with KPI and Line Charts
page_overview = vm.Page(
    title="Overview Dashboard",
    layout=vm.Layout(grid=[[0], [1], [1], [1]]),
    components=[kpi_container, line_charts_tabbed],
    controls=[
        vm.Filter(
            column="scale",
            targets=[],
            selector=vm.RadioItems(
                title="Select Scale",
                id="scale_selector",
                options=['hours', 'days', 'weeks'],
                value='days'
            )
        ),
        vm.Filter(
            column="ds",
            targets=[],
            selector=vm.DatePicker(
                range=True,
                title="Dates range",
                id='dates_selector_p1'
            )
        ),
    ]
)

# Page Queries counts detailed with heatmap
heatmap_tabbed = vm.Tabs(
    tabs=[
        vm.Container(
            title="Weekly queries count",
            components=[
                vm.Graph(
                    id="weekly_queries_count",
                    figure=heatmap_plot(
                        'heatmap_data', z="count",
                        title='Weekly queries count'
                    )
                )
            ]
        ),
        vm.Container(
            title="WoW difference",
            components=[
                vm.Graph(
                    id="wow_difference",
                    figure=heatmap_plot(
                        'heatmap_data', z="wow_diff",
                        title='WoW queries count difference'
                    )
                )
            ]
        ),
        vm.Container(
            title="WoW difference %",
            components=[
                vm.Graph(
                    id="wow_percentage_difference",
                    figure=heatmap_plot(
                        'heatmap_data', z="wow_diff_%",
                        title='WoW queries count difference %'
                    )
                )
            ]
        )
    ]
)

# Queries counts detailed layout with tabs
page_queries_detailed = vm.Page(
    title="Queries counts detailed",
    layout=vm.Layout(grid=[[0]]),
    components=[heatmap_tabbed],
    controls=[
        vm.Filter(
            column="ds",
            targets=[],
            selector=vm.DatePicker(
                range=True,
                title="Dates",
                id='dates_selector_p2'
            )
        ),
    ]
)

# Detailed Queries Text Page with table and charts
CELL_STYLE = {
    "styleConditions": [
        {
            "condition": "params.value < 0.05",
            "style": {"backgroundColor": "#21ba06"},
        },
    ]
}

COLUMN_DEFS = [
    {"field": "query"},
    {"field": "Count touch",
     "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
    {"field": "Count touch %",
     "valueFormatter": {"function": "d3.format(',.3%')(params.value)"}},
    {"field": "Count desktop",
     "valueFormatter": {"function": "d3.format(',.0f')(params.value)"}},
    {"field": "Count desktop %",
     "valueFormatter": {"function": "d3.format(',.3%')(params.value)"}},
    {"field": "P-value",
     "valueFormatter": {"function": "d3.format(',.3f')(params.value)"},
     "cellStyle": CELL_STYLE},
]

# Creating AgGrid for query data
table_grid = vm.AgGrid(
    id='ag',
    figure=dash_ag_grid(
        id='dag',
        data_frame='data_table',
        columnDefs=COLUMN_DEFS,
        defaultColDef={"resizable": False, "filter": True, "editable": False},
        dashGridOptions={"pagination": True, "paginationPageSize": 10},
        columnSize="responsiveSizeToFit"
    ),
    title=(
        "Queries counts and statistical significance of the difference "
        "between platforms"
    ),
)

# Butterfly Chart for platform percentage comparison
butterfly_chart = vm.Graph(
    id='btfly',
    figure=butterfly(
        'butterfly_data',
        x=["pct_desktop", "pct_touch"],
        y="query",
        labels={"value": "% of all", "variable": "platform:"},
        hover_name="query",
        hover_data={
            'query': False,
            'count_desktop': True,
            'count_touch': True
        },
    )
)

linechart_tabbed = vm.Tabs(
    tabs=[
        vm.Container(
            title="Queries platform: touch",
            components=[
                vm.Graph(
                    id='lchq_t',
                    figure=linechart_query_plot(
                        'query_linechart_data', platform='touch'
                    )
                )
            ]
        ),
        vm.Container(
            title="Queries platform: desktop",
            components=[
                vm.Graph(
                    id='lchq_d',
                    figure=linechart_query_plot(
                        'query_linechart_data', platform='desktop'
                    )
                )
            ]
        )
    ]
)

# Page layout for Queries Text Detailed
page_queries_text_detailed = vm.Page(
    title="Queries text detailed",
    layout=vm.Layout(grid=[[0, 1], [2, 1]]),
    components=[butterfly_chart, linechart_tabbed, table_grid],
    controls=[
        vm.Parameter(
            targets=[
                "ag.data_frame.date_range", 'btfly.data_frame.date_range',
                'lchq_t.data_frame.date_range', 'lchq_d.data_frame.date_range'
            ],
            selector=vm.DatePicker(
                range=True,
                title="Filter date range",
                id='date_filter',
                min='2021-09-01',
                max='2021-09-21',
                value=['2021-09-08', '2021-09-21']
            )
        ),
        vm.Parameter(
            targets=["ag.data_frame.min_cnt", 'btfly.data_frame.min_cnt'],
            selector=vm.Slider(
                title="Filter min sum query counts",
                id='min_query_count_filter',
                min=20,
                max=200,
                step=20,
                value=100
            )
        ),
    ]
)

description_tabbed = vm.Tabs(
    tabs=[
        vm.Container(
            title="RUS",
            components=[vm.Card(text=read_text("rus.txt"))]
        ),
        vm.Container(
            title="ENG",
            components=[vm.Card(text=read_text("eng.txt"))]
        ),
    ]
)

page_description = vm.Page(
    title="Project description",
    components=[description_tabbed],
)

# Final Dashboard setup with multiple pages and navigation
dashboard = vm.Dashboard(
    title="Yandex Queries Overview",
    pages=[
        page_overview,
        page_queries_detailed,
        page_queries_text_detailed,
        page_description
    ],
    navigation=vm.Navigation(
        nav_selector=vm.NavBar(
            items=[
                vm.NavLink(
                    label="Overview",
                    pages={
                        "Sections": [
                            "Overview Dashboard",
                            "Queries counts detailed",
                            "Queries text detailed"
                        ]
                    },
                    icon="bar_chart_4_bars"
                ),
                vm.NavLink(
                    label="Description",
                    pages=["Project description"],
                    icon="info"
                )
            ]
        )
    )
)

app = Vizro().build(dashboard)
server = app.dash.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
