import pandas as pd
import vizro.models as vm
from vizro.figures import kpi_card_reference, kpi_card
import vizro.plotly.express as px
from utils.data_loader import get_kpi_data, get_pie_data, agg_data
from vizro.models.types import capture
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# KPI Definitions
fig_kpi_date = vm.Figure(
    id="kpi-date",
    figure=kpi_card(
        agg_data,
        value_column='ds',
        value_format='{value}',
        agg_func='max',
        title='Date',
        icon="calendar_month"
    ),
)

fig_kpi_touch = vm.Figure(
    id="kpi-touch",
    figure=kpi_card_reference(
        get_kpi_data(agg_data, "touch"),
        value_column="actual",
        reference_column="previous",
        agg_func=lambda x: x.iloc[-1],
        title="Touch Queries",
        value_format="{value:,.0f}",
        reference_format="{delta_relative:+.1%} vs. previous ({reference:,.0f})",
        icon=["Smartphone"],
    ),
)

fig_kpi_desk = vm.Figure(
    id="kpi-desk",
    figure=kpi_card_reference(
        get_kpi_data(agg_data, "desktop"),
        value_column="actual",
        reference_column="previous",
        agg_func=lambda x: x.iloc[-1],
        title="Desktop Queries",
        value_format="{value:,.0f}",
        reference_format="{delta_relative:+.1%} vs. previous ({reference:,.0f})",
        icon=["computer"],
    ),
)

fig_graph_pie = vm.Graph(
    figure=px.pie(
        data_frame=get_pie_data(agg_data),
        values="count",
        names="platform",
        title="Queries Ratio Over Selected Date Range",
    )
)

@capture("graph")
def outliers_line_plot(data_frame: pd.DataFrame, **kwargs) -> go.Figure:
    """
    Create a line plot highlighting outliers outside the 95% confidence interval.

    Args:
        data_frame (pd.DataFrame): Data to plot.

    Returns:
        go.Figure: Plotly figure with outliers.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data_frame['ds'], y=data_frame['y'], name="Actual", mode='markers',
        customdata=data_frame['ds'].dt.day_name(),
        hovertemplate="<b>Date:</b> %{x}<br><b>Actual:</b> %{y}<br><b>DOW:</b> %{customdata}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=data_frame['ds'], y=data_frame['yhat'], name="Prediction", mode='lines',
        customdata=data_frame['ds'].dt.day_name(),
        hovertemplate="<b>Date:</b> %{x}<br><b>Prediction:</b> %{y:.0f}<br><b>DOW:</b> %{customdata}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=data_frame['ds'], y=data_frame['yhat_lower'], fill='tonexty', mode='none', name="95% CI Lower",
        customdata=data_frame['ds'].dt.day_name(),
        hovertemplate="<b>Date:</b> %{x}<br><b>95% CI Lower:</b> %{y:.0f}<br><b>DOW:</b> %{customdata}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=data_frame['ds'], y=data_frame['yhat_upper'], fill='tonexty', mode='none', name="95% CI Upper",
        customdata=data_frame['ds'].dt.day_name(),
        hovertemplate="<b>Date:</b> %{x}<br><b>95% CI Upper:</b> %{y:.0f}<br><b>DOW:</b> %{customdata}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(x=data_frame['ds'], y=data_frame['trend'], name="Trend"))

    fig.update_layout(
        yaxis=dict(title="Number of Queries"),
        title="Outliers Outside the 95% Confidence Interval"
    )
    return fig

@capture("graph")
def components_plot(data_frame: pd.DataFrame, **kwargs) -> go.Figure:
    """
    Plot the components of a time series model (Trend, Weekly, and Daily Seasonality).

    Args:
        data_frame (pd.DataFrame): Data containing model components.

    Returns:
        go.Figure: Plotly figure with model components.
    """
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=["Trend", "Weekly Seasonality", "Daily Seasonality"]
    )

    fig.add_trace(go.Scatter(
        x=data_frame['ds'], y=data_frame['trend'], mode='lines', name='Trend',
        hovertemplate="<b>Date:</b> %{x}<br><b>Trend:</b> %{y:.0f}<extra></extra>",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=data_frame['ds'][-168:], y=data_frame['weekly'][-168:], mode='lines', name='Weekly Trend',
        customdata=data_frame['ds'].dt.day_name(),
        hovertemplate="<b>Date:</b> %{x}<br><b>Weekly Trend:</b> %{y:.0f}<br><b>DOW:</b> %{customdata}<extra></extra>",
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=data_frame['ds'][-24:], y=data_frame['daily'][-24:], mode='lines', name='Daily Trend',
        hovertemplate="<b>Time:</b> %{x}<br><b>Daily Trend:</b> %{y:.0f}<extra></extra>",
    ), row=3, col=1)

    fig.update_layout(title="Model Components", showlegend=False)
    return fig

@capture("graph")
def heatmap_plot(data_frame: pd.DataFrame, z: str, **kwargs) -> go.Figure:
    """
    Create a heatmap to visualize data over time and by hour.

    Args:
        data_frame (pd.DataFrame): Data for the heatmap.
        z (str): Column to use for intensity.

    Returns:
        go.Figure: Plotly heatmap figure.
    """
    df = data_frame[data_frame.date > data_frame.date.max() - pd.Timedelta(7, 'days')]

    color_scale = px.colors.diverging.BrBG if z == 'wow_diff_%' else px.colors.sequential.Purples
    fig = px.density_heatmap(
        df, x="date", y="hour", z=z, histfunc="sum",
        text_auto=True, nbinsy=24, nbinsx=7, facet_col="platform",
        color_continuous_scale=color_scale,
        color_continuous_midpoint=0 if z == 'wow_diff_%' else None,
        **kwargs
    )

    hover_template = '<b>Date: </b>%{x}<br><b>Hour: </b>%{y}<br><b>Queries count: </b>%{z:.2f}%' if z == 'wow_diff_%' else '<b>Date: </b>%{x}<br><b>Hour: </b>%{y}<br><b>Queries count: </b>%{z}'
    text_template = '%{z:.2f}%' if z == 'wow_diff_%' else '%{z}'

    for data in fig.data:
        data.hovertemplate = hover_template
        data.texttemplate = text_template

    fig.update_coloraxes(colorbar_ticksuffix='%' if z == 'wow_diff_%' else '')
    fig.update_coloraxes(colorbar_title_text='')
    return fig

@capture("graph")
def butterfly(data_frame: pd.DataFrame, **kwargs) -> go.Figure:
    """
    Create a butterfly chart for comparing platform percentages.

    Args:
        data_frame (pd.DataFrame): Data for the chart.

    Returns:
        go.Figure: Butterfly chart.
    """
    fig = px.bar(
        data_frame.iloc[::-1], color_discrete_sequence=px.colors.qualitative.D3[1::-1], **kwargs
    )

    orientation = fig.data[0].orientation
    x_or_y = "x" if orientation == "h" else "y"

    fig.update_traces({f"{x_or_y}axis": f"{x_or_y}2"}, selector=1)
    fig.update_layout({
        f"{x_or_y}axis": {"autorange": "reversed", "domain": [0, 0.5], "title": None},
        f"{x_or_y}axis2": {"domain": [0.5, 1], "title": None},
        "legend": {
            "x": 0,
            "y": 0,
            "xanchor": "left",
            "yanchor": "bottom",
            "orientation": "v"
        }
    })

    if orientation == "h":
        fig.add_vline(x=0, line_width=2, line_color="grey")
    else:
        fig.add_hline(y=0, line_width=2, line_color="grey")

    fig.data[0].hovertemplate = '<b>%{hovertext}</b><br><b>% </b>=%{x:.2%}<br><b>Qty</b>=%{customdata[0]}'
    fig.data[1].hovertemplate = '<b>%{hovertext}</b><br><b>% </b>=%{x:.2%}<br><b>Qty</b>=%{customdata[0]}'
    fig.update_layout(
        margin=dict(l=20, r=20, t=0, b=0),
    )
    return fig

@capture("graph")
def linechart_query_plot(data_frame: pd.DataFrame, platform='touch', **kwargs) -> go.Figure:
    """
    Create a line chart showing queries by hour for a given platform.

    Args:
        data_frame (pd.DataFrame): Data for the line chart.
        platform (str): Platform to filter by (e.g., 'touch' or 'desktop').

    Returns:
        go.Figure: Line chart for queries.
    """
    df = data_frame.query("platform==@platform")
    fig = px.line(
        df,
        x='hour',
        y='count',
        color='query',
        **kwargs
    )

    fig.update_layout(
        title={
            "text": "Dynamics in number of popular search queries by hour",
            "x": 0.5,
            "xanchor": 'center'
        },
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5
        ),
    )
    fig.for_each_annotation(lambda a: a.update(text=f"Platform: {a.text}"))
    fig.update_layout(margin=dict(l=20, r=20, t=0, b=20))
    for axis in fig.layout:
        if axis.startswith("yaxis"):
            fig.layout[axis].matches = None

    return fig
