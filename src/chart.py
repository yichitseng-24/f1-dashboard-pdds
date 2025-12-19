import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import src.data_handler as data_handler 
import src.layouts as layouts 


# --- Define Visualize Function ------

# empty figure 1 : no driver selected
no_driver_fig = go.Figure()
no_driver_fig.update_layout(
    title="No driver selected", title_font=dict(size=23),
    plot_bgcolor='rgba(0,0,0,0)')
no_driver_fig.update_xaxes(showticklabels=False, showline=False)
no_driver_fig.update_yaxes(showticklabels=False, showline=False)

# empty figure 2 : no data for selected year/drivers
no_data_fig = go.Figure()
no_data_fig.update_layout(
    title="No data for selected year/driver(s)", title_font=dict(size=23),
    plot_bgcolor='rgba(0,0,0,0)')
no_data_fig.update_xaxes(showticklabels=False, showline=False)
no_data_fig.update_yaxes(showticklabels=False, showline=False)

# 1 Ranking Evolution: Chart
def create_ranking_evolution_figure(selected_year, selected_drivers):
    if not selected_drivers:
        return no_driver_fig
    df = data_handler.get_ranking_evolution_data(selected_year, selected_drivers)
    if df.empty:
        fig = go.Figure()
        return no_data_fig

    df = df.sort_values(["driver_id", "round"])
    fig = go.Figure()
    for driver in df["driver_id"].unique():
        sub = df[df["driver_id"] == driver]
        team = str(sub["team"].iloc[0])
        driver_name = str(driver.split("-")[-1].capitalize())


        team_color = layouts.PLOTLY_TEAM_COLOR_MAP.get(team, "#808080")
        fig.add_trace(
            go.Scatter(
                x=sub["round"],
                y=sub["points"],
                mode="lines+markers",
                name=f"{driver} ({team})",  
                legendgroup=team,
                line=dict(color=team_color),
                hovertemplate=
                    " "+ driver_name + " <br>" +
                    " Team: " + team + " <br>" +
                    " Round: %{x} <br>" +
                    " Points: %{y} " +
                    " <extra></extra> ",
                hoverlabel=dict(font=dict(size=16))
            )
        )

        max_round = sub["round"].max() 
        x_range_max = max_round + 0.5 
        x_range_min = 0.5
    
    fig.update_layout(
        xaxis_title="Round",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(tickmode='linear',
                   range=[x_range_min, x_range_max],),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(150, 150, 150, 0.2)',
            zeroline=False
        ),
        margin=dict(l=50, r=30, b=50, t=30, pad=4),
        annotations=[
        dict(
            x=-0.025, 
            y=0.975,  
            xref="paper",     
            yref="paper",     
            text='Points',
            showarrow=False,  
            font=dict(size=16, color='gray'), 
            textangle=0,      
            xanchor='left', 
            yanchor='bottom'  
        )
        ]

    )
    fig.update_xaxes(title_font={'size': 16, 'color':'gray'})
    return fig


# 2 Driver stability: Chart
def create_nvr_figure(selected_year, selected_drivers):
    if not selected_drivers:
        return no_driver_fig
    df = data_handler.get_not_valid_race_data(selected_year, selected_drivers)
    
    if df.empty:
        return no_data_fig
    
    df['stability'] = 1 - df['nvr']
    
    df_sorted = df.sort_values(by='stability', ascending=False)
    current_drivers = df_sorted['driver'].tolist()
    team_colors = [
        layouts.PLOTLY_TEAM_COLOR_MAP.get(team_name, '#CCCCCC') 
        for team_name in df['team']
    ]
    
    trace = go.Bar(
        x=df['driver'], 
        y=df['stability'],
        marker=dict(
            color=team_colors 
        ),
        customdata=df[['total_race_count']],
        hovertemplate=(
            " <b>%{x}</b><br>" + 
            " Stability: %{y:.2%} <br>" +
            " Total Races: %{customdata[0]} <extra></extra>"
        ),
        hoverlabel=dict(font=dict(size=16))
    )
    
    fig = go.Figure(data=[trace])
    
    fig.update_layout(
        hoverlabel=dict(font=dict(size=14)),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False, 
        margin=dict(l=30, r=30, b=30, t=30, pad=4),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(150, 150, 150, 0.2)',
            zeroline=False
        ),
        annotations=[
        dict(
            x=-0.04, 
            y=0.99,  
            xref="paper",     
            yref="paper",     
            text='Finish rate',
            showarrow=False,  
            font=dict(size=16, color='gray'), 
            textangle=0,      
            xanchor='left', 
            yanchor='bottom'  
        )]
    )
    
    fig.update_xaxes(
        title_text='',
        categoryorder='array', 
        categoryarray=current_drivers,
        tickangle=0,
        tickfont=dict(size=14)
    ) 
    
    fig.update_yaxes(
        tickformat=".0%", 
        range=[0, 1.05],
    )

    return fig

# 3 Pace Stability: Chart
def create_pace_stability_figure(selected_year, selected_drivers):
    if not selected_drivers:
        return no_driver_fig
    df = data_handler.get_race_pace_data(selected_year, selected_drivers)
    
    if df.empty:
        return no_data_fig
    
    df = data_handler.remove_outliers_from_pace_data(df)
    global_mean = np.mean(df["lap_time_sec"])

    stats_df = df.groupby("driver")["lap_time_sec"].agg(
        min_val='min',
        mean_val='mean',
        max_val='max',
        q1= lambda x: x.quantile(0.25),
        median='median',
        q3=lambda x: x.quantile(0.75),
    )
    iqr_values = stats_df['q3'] - stats_df['q1']
    order = (iqr_values.sort_values(ascending=True).index.tolist())
    
    fig = go.Figure()

    for team, team_df in df.groupby('team'):
        team_color = layouts.PLOTLY_TEAM_COLOR_MAP.get(team, '#888')
        fig.add_trace(
            go.Box(
                x=team_df['driver'],
                y=team_df['lap_time_sec'],
                name=team,
                marker_color=team_color,
                width=0.9,
                boxpoints=False,
                line=dict(width=1.8),
                quartilemethod='inclusive',
                hoverinfo='skip' # ignore Box Trace hover
            )
        )
    
    hover_df = stats_df.reset_index().merge(df[['driver', 'team']].drop_duplicates(), on='driver', how='left')
    hover_customdata = hover_df[['min_val', 'mean_val','max_val', 'q1', 'median', 'q3']].values
    driver_team_colors = [
        layouts.PLOTLY_TEAM_COLOR_MAP.get(team_name, '#CCCCCC') 
        for team_name in hover_df['team']
    ]

    fig.add_trace(
        go.Scatter(
            x=hover_df['driver'],
            y=hover_df['median'], 
            mode='markers',
            marker=dict(color=driver_team_colors, size=1), # invisible dot
            name="Hover Stats", 
            customdata=hover_customdata,
            hovertemplate=(
                    "<br>"
                    "  <b>%{x}</b><br>"
                    "  Best: %{customdata[0]:.2f}   </b><br>"
                    "  Average: %{customdata[1]:.2f}   </b><br>"
                    "  Worst: %{customdata[2]:.2f}   </b><br>"
                    "<br>"
                    "  25%: %{customdata[3]:.2f}   <br>"
                    "  50%:  %{customdata[4]:.2f}   <br>"
                    "  75%: %{customdata[5]:.2f}   <br>"
                    "<extra></extra>"
            ),
            hoverlabel=dict(font=dict(size=16)),
        )
    )

    fig.add_hline(
        y=global_mean, 
        line_dash="dash",
        line_color="#7A7A7A",
        line_width=1.5,
        layer="below"
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=10, r=10, b=10, t=20, pad=4),
        annotations=[
            dict(
                x=-0.03, y=0.975, xref="paper", yref="paper", 
                text='Lap Time (s)', showarrow=False,  
                font=dict(size=16, color='gray'), 
                textangle=0, xanchor='left', yanchor='bottom'  
            )
        ]
    )

    fig.update_xaxes(
        tickangle=0,
        tickfont=dict(size=14),
        categoryorder='array',
        categoryarray=order,
        range=[-0.5, len(order) - 0.5], #
        showgrid=False 
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridcolor='#e0e0e0',
    )
    return fig

# 4 Position Flow Stability: Chart
def visualize_position_flow_chart(df):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig

    filter_mask = (
        df["grid_position_text"].notna()
        & df["position_text"].notna()
        & df["grid_position_text"].str.isdigit()
        & df["position_text"].str.isdigit()
    )
    df = df[filter_mask].copy()

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No numeric positions available",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig

    df["start"] = df["grid_position_text"].astype(int)
    df["finish"] = df["position_text"].astype(int)

    start_unique = sorted(df["start"].unique())
    finish_unique = sorted(df["finish"].unique())

    start_labels = [f"P{v}" for v in start_unique]
    finish_labels = [f"P{v}" for v in finish_unique]
    labels = start_labels + finish_labels

    def spaced_positions(n, top=0.02, bottom=0.98):
        if n <= 1:
            return [0.5]
        step = (bottom - top) / (n - 1)
        return [top + i * step for i in range(n)]

    y_start = spaced_positions(len(start_unique))
    y_finish = spaced_positions(len(finish_unique))

    node_x = [0.0001] * len(start_unique) + [0.9999] * len(finish_unique)
    node_y = y_start + y_finish

    start_index = {v: i for i, v in enumerate(start_unique)}
    finish_index = {v: i + len(start_unique) for i, v in enumerate(finish_unique)}

    flow = df.groupby(["start", "finish"], as_index=False).size()
    source = [start_index[s] for s in flow["start"]]
    target = [finish_index[f] for f in flow["finish"]]
    values = flow["size"].tolist()
    
    COLOR_UP ="rgba(46,204,113,0.40)"   # green: finish < start
    COLOR_SAME = "rgba(176,176,176,0.40)"  # grey: finish == start
    COLOR_DOWN = "rgba(231,76,60,0.40)"   # red: finish > start

    link_colors = []
    for s, f in zip(flow["start"], flow["finish"]):
        if f < s:
            link_colors.append(COLOR_UP)
        elif f == s:
            link_colors.append(COLOR_SAME)
        else:
            link_colors.append(COLOR_DOWN)
    
    node_colors = ["#828282"] * len(labels)

    fig = go.Figure(
        go.Sankey(
            arrangement="fixed",
            node=dict(
                line=dict(width=0),
                pad=25,
                thickness=12,
                label=labels,
                color=node_colors,
                x=node_x,
                y=node_y,
            ),
            link=dict(source=source, target=target, value=values, color=link_colors),
        )
    )

    fig.update_layout(
        font=dict(size=14),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=30, r=30, b=80, t=60, pad=4),
        annotations=[
            dict(
                x=-0.01, 
                y=1.1,    
                text='Start', 
                showarrow=False, 
                xref="paper",   
                yref="paper",     
                font=dict(size=15, color="gray"),
            ),
            
            dict(
                x=1.01,
                y=1.1,
                text='Finish',
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=15, color="gray")
            ),
            # Legend annotations
            dict(
                x=0.2,
                y=-0.15,
                text='<span style="color:#82E0AA;">●</span> Positions Gained',
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=18),
                align='left'
            ),
            dict(
                x=0.52,
                y=-0.15,
                text='<span style="color:#808080;">●</span> Position Unchanged',
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=18),
                align='center'
            ),
            dict(
                x=0.82,
                y=-0.15,
                text='<span style="color:#FF0000;">●</span> Positions Lost',
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=18),
                align='right'
            )
        ]
    )
    fig.update_traces(
        link=dict(
            hovertemplate=' Start %{source.label} to Finish %{target.label} <br> %{value:.0} race<extra></extra>',
            hoverlabel=dict(font=dict(size=16)),
        ),
        node=dict(
            hovertemplate=' %{label} <br> %{value:.0} <extra></extra>',
            hoverlabel=dict(font=dict(size=16)),
        )
    )

    return fig



