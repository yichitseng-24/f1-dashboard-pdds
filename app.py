# app.py 
import dash
<<<<<<< HEAD
from dash import Input, Output, ALL, State, dcc, html,  no_update
=======
from dash import Input, Output, MATCH, ALL, State, dcc, html, dash_table, callback_context, no_update
>>>>>>> origin/master
import src.layouts as layouts 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import src.data_handler as data_handler 

<<<<<<< HEAD

=======
>>>>>>> origin/master
# Import font 'Inter'
external_stylesheets = [ 
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"
]

# Initialize Dash 
<<<<<<< HEAD
# Dash 會自動尋找並載入 assets/f1_styles.css
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True # 啟用這項以支援 Tab 切換時的動態內容
=======
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
>>>>>>> origin/master
)

# Dashboard layout
app.layout = layouts.full_page_layout

# --- Define Visualize Function ------

# 1 Ranking Evolution: Chart
def create_ranking_evolution_figure(selected_year, selected_drivers):
    df = data_handler.get_ranking_evolution_data(selected_year, selected_drivers)
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data for selected year/driver(s)",
            xaxis_title="Round",
            yaxis_title="Points"
        )
        return fig

    df = df.sort_values(["driver_id", "round"])
    fig = go.Figure()
    for driver in df["driver_id"].unique():
        sub = df[df["driver_id"] == driver]
        team = sub["team"].iloc[0]
        driver_name = driver.split("-")[-1].capitalize()
<<<<<<< HEAD
        team_color = layouts.PLOTLY_TEAM_COLOR_MAP.get(team, "#808080") # 使用灰色作為默認顏色
=======
        team_color = layouts.PLOTLY_TEAM_COLOR_MAP.get(team, "#808080")
>>>>>>> origin/master
        fig.add_trace(
            go.Scatter(
                x=sub["round"],
                y=sub["points"],
                mode="lines+markers",
                name=f"{driver} ({team})",  
                legendgroup=team,
                line=dict(color=team_color),
                hovertemplate=
<<<<<<< HEAD
                    #"<span style='color:" + team_color + "'><b>%{text}</b></span><br>" +
                    driver_name + "<br>" + #may be a bug
=======
                    driver_name + "<br>" +
>>>>>>> origin/master
                    "Team: " + team + "<br>" +
                    "Round: %{x}<br>" +
                    "Points: %{y}<br>" +
                    "<extra></extra>"
            )
        )
<<<<<<< HEAD
        # add here
        max_round = sub["round"].max() 
        x_range_max = max_round + 0.5 
        x_range_min = 0.5
=======

        max_round = sub["round"].max() 
        x_range_max = max_round + 0.5 
        x_range_min = 0.5
    
>>>>>>> origin/master
    fig.update_layout(
        xaxis_title="Round",
        yaxis_title="Points",
        legend_title="Driver",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
<<<<<<< HEAD
        xaxis=dict(
            tickmode='linear',
            range=[x_range_min, x_range_max], #add here
            #dtick=1
        ),
        # add here
=======
        xaxis=dict(tickmode='linear',
                   range=[x_range_min, x_range_max],),
>>>>>>> origin/master
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(150, 150, 150, 0.2)',
            zeroline=False
        ),
<<<<<<< HEAD
        margin=dict(
            l=30,  # Left margin
            r=30,  # Right margin
            b=30,  # Bottom margin
            t=30,  # Top margin 
            pad=4   # Padding
        ),
    )
    fig.update_xaxes(
        title_font={'size': 18}
        ) 
    fig.update_yaxes(
        title_font={'size': 18})
    return fig


# 2 Driver Instability: Chart
def create_nvr_figure(selected_year, selected_drivers):
    fig = go.Figure()
    if not selected_drivers:
        return fig
    try:
        df = data_handler.get_not_valid_race_data(selected_year, selected_drivers)
    except Exception:
        return fig
    
    if df.empty:
=======
        margin=dict(l=30, r=30, b=30, t=30, pad=4),

    )
    fig.update_xaxes(title_font={'size': 18})
    fig.update_yaxes(title_font={'size': 18})
    return fig

# 2 Driver Instability: Chart
def create_nvr_figure(selected_year, selected_drivers):
    df = data_handler.get_not_valid_race_data(selected_year, selected_drivers)
    
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data for selected year/driver(s)",
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
        )
>>>>>>> origin/master
        return fig
    
    df_sorted = df.sort_values(by='nvr', ascending=False)
    current_drivers = df_sorted['driver'].tolist()
    
    fig = px.bar(df, x='driver', y='nvr', 
<<<<<<< HEAD
                 color='team', color_discrete_map=layouts.PLOTLY_TEAM_COLOR_MAP,
                 template='plotly'
    )
    fig.update_layout(
        hoverlabel=dict(
            font=dict(
                size=14
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
=======
                 color='team', color_discrete_map=layouts.PLOTLY_TEAM_COLOR_MAP)
    
    fig.update_layout(
        hoverlabel=dict(font=dict(size=14)),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=30, r=30, b=30, t=30, pad=4),
>>>>>>> origin/master
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(150, 150, 150, 0.2)',
            zeroline=False
<<<<<<< HEAD
        )
    )
=======
        ),
    )
    
>>>>>>> origin/master
    fig.update_xaxes(
        title_text='',
        categoryorder='array',
        categoryarray=current_drivers
<<<<<<< HEAD
        ) 
    fig.update_yaxes(
        title_text='Percentage of Not Valid Race',
        title_font={'size': 18})
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Not Valid Race: %{y}<extra></extra>" 
    )
    return fig


# 3 Pace Stability: Chart
"""stella's code"""



# 4 Position Flow Stability: Chart
"""lam's code"""
def visualize_position_flow_chart(df):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data available")
=======
    ) 
    
    fig.update_yaxes(
        title_text='Percentage of Not Valid Race',
        title_font={'size': 18},
        tickformat=".0%"
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Not Valid Race: %{y:.1%}<extra></extra>"
    )

    return fig

# 3 Pace Stability: Chart
def create_pace_stability_figure(selected_year, selected_drivers, selected_race=None):
    if not selected_drivers:
        fig = go.Figure()
        fig.update_layout(
            title="No drivers selected",
            xaxis_title="Driver",
            yaxis_title="Lap Time (seconds)",
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=30, r=30, b=30, t=30, pad=4),
        )
        fig.update_xaxes(title_font={'size': 18})
        fig.update_yaxes(title_font={'size': 18})
        return fig

    df = data_handler.get_race_pace_data(selected_year, selected_drivers, selected_race)
    
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data for selected year/driver(s)",
            xaxis_title="Driver",
            yaxis_title="Lap Time (seconds)",
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=30, r=30, b=30, t=30, pad=4),
        )
        fig.update_xaxes(title_font={'size': 18})
        fig.update_yaxes(title_font={'size': 18})
        return fig
    
    df = data_handler.remove_outliers_from_pace_data(df)
    
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No valid data after outlier removal",
            xaxis_title="Driver",
            yaxis_title="Lap Time (seconds)"
        )
        return fig
    
    order = (
        df.groupby("driver")["lap_time_sec"]
            .median()
            .sort_values()
            .index.tolist()
    )
    
    fig = px.box(
        df, 
        x="driver", 
        y="lap_time_sec",
        color="team",
        color_discrete_map=layouts.PLOTLY_TEAM_COLOR_MAP,
        category_orders={"driver": order},
    )

    fig.update_traces(width=0.9)
    
    fig.update_layout(
        xaxis_title="Driver",
        yaxis_title="Lap Time (seconds)",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=30, r=30, b=30, t=30, pad=4),
    )
    fig.update_xaxes(title_font={'size': 18})
    fig.update_yaxes(title_font={'size': 18})
    
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
>>>>>>> origin/master
        return fig

    df = df[
        df["grid_position_text"].notna()
        & df["position_text"].notna()
        & df["grid_position_text"].str.isdigit()
        & df["position_text"].str.isdigit()
    ].copy()

    if df.empty:
        fig = go.Figure()
<<<<<<< HEAD
        fig.update_layout(title="No numeric positions")
=======
        fig.update_layout(
            title="No numeric positions available",
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
>>>>>>> origin/master
        return fig

    df["start"] = df["grid_position_text"].astype(int)
    df["finish"] = df["position_text"].astype(int)

    start_unique = sorted(df["start"].unique())
    finish_unique = sorted(df["finish"].unique())

    start_labels = [f"Start {v}" for v in start_unique]
    finish_labels = [f"Finish {v}" for v in finish_unique]
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

    colors = [
        ("#4F46E5", "rgba(79,70,229,0.35)"),
        ("#0EA5E9", "rgba(14,165,233,0.35)"),
        ("#10B981", "rgba(16,185,129,0.35)"),
        ("#F59E0B", "rgba(245,158,11,0.35)"),
        ("#F43F5E", "rgba(244,63,94,0.35)"),
        ("#8B5CF6", "rgba(139,92,246,0.35)"),
    ]

    node_colors = [colors[i % len(colors)][0] for i in range(len(labels))]
    link_colors = [colors[start_index[s] % len(colors)][1] for s in flow["start"]]

    fig = go.Figure(
        go.Sankey(
            arrangement="fixed",
            node=dict(
                pad=25,
                thickness=18,
                label=labels,
                color=node_colors,
                x=node_x,
                y=node_y,
            ),
            link=dict(source=source, target=target, value=values, color=link_colors),
        )
    )

    fig.update_layout(
        title=f"Start → Finish Flow — {df['driver_name'].iloc[0]} ({df['year'].iloc[0]})",
        font=dict(size=14),
        paper_bgcolor="white",
        plot_bgcolor="white",
<<<<<<< HEAD
=======
        margin=dict(l=30, r=30, b=30, t=60, pad=4),
>>>>>>> origin/master
    )
    return fig

# ------ callback ----------

<<<<<<< HEAD
# 0 show driver dropdown when tab4
@app.callback(
    Output('driver-dropdown', "style"),
    Input('main-nav-tabs', "value")
)
def toggle_dropdown(tab_id):
    if tab_id == 'position-flow-stability':
        return {'display': 'block', 'width': '200px'}
    else:
        return {"display": "none", "width": "200px"}


# 1 Render left page (titles, dropdowns, main chart)
@app.callback(
    Output('main-container-left', 'children'),
    [
        Input('main-nav-tabs', 'value')
    ],
    [State('year-dropdown', 'value')]
    )
def render_page_content(tab_id, year):
    # Create left-side content (Title, Dropdown, Chart)
    content_area = layouts.create_content_area(tab_id, year) 
    return content_area

# 1.1 Update titles according to tab_id (May be improved)
@app.callback(
        [
            Output('page-title-h1','children'),
            Output('page-subtitle-p', 'children')
        ],
        Input('main-nav-tabs', 'value')
=======
# 1 Render left page (titles, dropdowns, main chart)
@app.callback(
    Output('main-container-left', 'children'),
    Input('main-nav-tabs', 'value'),
    State('year-dropdown', 'value')
)
def render_page_content(tab_id, year):
    content_area = layouts.create_content_area(tab_id, year) 
    return content_area

# 1.1 Update titles according to tab_id
@app.callback(
    Output('page-title-h1','children'),
    Output('page-subtitle-p', 'children'),
    Input('main-nav-tabs', 'value')
>>>>>>> origin/master
)
def update_title(tab_id):
    title, subtitle = layouts.get_tab_titles(tab_id) 
    return title, subtitle 

<<<<<<< HEAD

# 2 Render right page (driver selection table, cards)
@app.callback(
        Output('main-container-right', 'children'),
        [
            Input('main-nav-tabs', 'value'),
            Input('year-dropdown', 'value'),
            Input('selected-drivers-store', 'data'),
            Input('driver-dropdown', 'value'), 
        ]
)
def get_sidebar(tab_id, selected_year, stored_drivers, selected_driver):
    # Create right-side content
    
    if tab_id in ['ranking-evolution', 'driver-instability', 'pace-stability']:
        # For the first three tabs, show dynamic driver selection table
=======
# 2 Render right page (driver selection table, cards)
@app.callback(
    Output('main-container-right', 'children'),
    Input('main-nav-tabs', 'value'),
    Input('year-dropdown', 'value'),
    Input('selected-drivers-store', 'data'),
    
)
def get_sidebar(tab_id, selected_year, stored_drivers):
    # Create right-side content
    
    if tab_id in ['ranking-evolution', 'driver-instability', 'pace-stability']:
>>>>>>> origin/master
        try:
            df_drivers = data_handler.get_proper_format(selected_year)
        except:
            df_drivers = pd.DataFrame({'Team_Code': ['---'], 'Driver_Name': ['---'], 'Points': ['---']})
            
        sidebar = layouts.create_driver_list_panel(df_drivers, stored_drivers)
        
    elif tab_id == 'position-flow-stability':
<<<<<<< HEAD
        # For tab 4, show information cards: Not Yet Finished
        sidebar = layouts.create_summary_cards()
        
    else:
        # In case of error
=======
        sidebar = layouts.create_summary_cards()
        
    else:
>>>>>>> origin/master
        sidebar = html.Div("Not Found")
    
    return sidebar

<<<<<<< HEAD

# 3 Selected drivers memory
# In order to store the selected driver when switching tabs
@app.callback(
    Output('selected-drivers-store', 'data'),
    Input({'type': 'driver-checkbox', 'index': ALL}, 'value'),
)
def update_selected_drivers(values):
    selected = []
    for v in values:
        if v and len(v) > 0:
            selected.append(v[0])
    return selected

# 4 Update the driver menu
@app.callback(
        Output('driver-dropdown', 'options'),
        Output('driver-dropdown', 'value'),
        [Input('year-dropdown', 'value')]
)
def update_driver_dropdown_options(year):
    if not year:
        return [], None
    df = data_handler.get_proper_format(year)   # có cả driver_id và driver
    options = [
        {
            'label': html.Div([
                html.Span('Driver', style={
                    'fontWeight': '500',
                    'fontSize': '0.9em',
                    'color': "#9f9f9f",
                    'marginRight': '6px'
                }),
                html.Span(row['driver'])  # chữ đẹp để hiển thị
            ], style={'display': 'flex', 'alignItems': 'center'}),
            'value': row['driver']      # here we have to decide to us driver 'Alonso' or driver-id 'fernando-alonso'
                                        # driver last name -> change lam's sql or output data
                                        # driver-id -> change update-cards's matching logic
        }
        for _, row in df.iterrows()
    ]

    new_default_value = df['driver'].iloc[0] if not df.empty else None
    return options, new_default_value



# 4 Update main chart
# According to tab_id and selected_year, selected_drivers
@app.callback(
        Output('main-chart-graph', 'figure'),
        [
        Input('main-nav-tabs', 'value'),
        Input('year-dropdown', 'value'),
        Input({'type': 'driver-checkbox', 'index': ALL}, 'value'),
        #Input('driver-dropdown', 'value'), 
        ]
        )
def update_main_figure(tab_id, selected_year, driver_list): #selected-single-driver
    
    # Driver list looks like :[['pierre-gasly'], [], ['yuki-tsunoda'], [], ['Alonso']]
    selected_drivers = []
    for sublist in driver_list:
        for element in sublist:
            selected_drivers.append(element)
   

    # Call the visualization function according to tab_id, selected_year,selected_drivers
    
    # 1 Ranking evolution
    if tab_id == 'ranking-evolution':
       figure_object = create_ranking_evolution_figure(selected_year, selected_drivers)
       return figure_object
    
    # 2 Driver Instability
    if tab_id == 'driver-instability':
       figure_object = create_nvr_figure(selected_year, selected_drivers)
       return figure_object

    """
    3 Pace Stability
    if tab_id == '':
       figure_object = 
       return figure_object
    
    4 Position Flow Stability
    if tab_id == '':
       figure_object = 
       return figure_object
    """
    #4 Position Flow Stability
    """if tab_id == 'position-flow-stability':
        if selected_year is None or selected_single_driver is None:
            return go.Figure()
        df = data_handler.get_position_flow_data(selected_year, selected_single_driver)
        return visualize_position_flow_chart(df)"""
    
    return go.Figure()

# Update the cards (Tab4)
@app.callback(
    [
        Output('card-points-value','children'),
        Output('card-instability-value','children'),
        Output('card-pace-value','children')
    ],
    [
        Input('year-dropdown', 'value'),
        Input('driver-dropdown','value'), #driver-input : 'Alonso', 'Gasly'
        Input('main-nav-tabs','value')
    ],
    prevent_initial_call=True
)
def update_cards(year, driver, tab_id):
    if tab_id != 'position-flow-stability':
        return no_update, no_update, no_update
    df_driver = data_handler.get_proper_format(year)
    row = df_driver[df_driver['driver']==driver]
    if row.empty:
        points = "N/A"
        driver_id = None
    else:
        points = row['total_points'].iloc[0]
        driver_id = row['driver_id'].iloc[0]
    if driver_id is not None:
        driver_list = [driver_id]
        try:
            instab_df = data_handler.get_not_valid_race_data(year, driver_list)
            if not instab_df.empty and 'nvr' in instab_df.columns:
                instab_value = instab_df['nvr'].iloc[0]
                instab = f"{instab_value:.2f}"
            else:
                instab = "N/A"
        except Exception:
            instab = "N/A"
    else:
        instab = "N/A"
    """
    try:
        pace = get_race_pace_data()
    else:
        pace = "N/A"
    """
    pace = "N/A" # for test
    return str(points), str(instab), str(pace)

# Run app
if __name__ == '__main__':
    # Set debug=True
    app.run(debug=True)

=======
# 3 Selected drivers memory
@app.callback(
    Output('selected-drivers-store', 'data'),
    Input({'type': 'driver-checkbox', 'index': ALL}, 'value'),
    Input('select-all-button', 'n_clicks'),
    Input('clear-all-button', 'n_clicks'),
    State('year-dropdown', 'value'),
    State('selected-drivers-store', 'data'),
    prevent_initial_call=True
)
def update_selected_drivers(checkbox_values, select_all_clicks, clear_all_clicks, selected_year, current_selected):
    ctx = callback_context
    
    if not ctx.triggered:
        return current_selected
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'select-all-button' and select_all_clicks:
        df_drivers = data_handler.get_proper_format(selected_year)
        all_driver_ids = df_drivers['driver_id'].tolist()
        return all_driver_ids
    
    elif triggered_id == 'clear-all-button' and clear_all_clicks:
        return []
    
    else:
        selected = []
        for v in checkbox_values:
            if v and len(v) > 0:
                selected.append(v[0])
        return selected

# 4 Main chart callback - Simplified version without conditional dropdowns
@app.callback(
    Output('main-chart-graph', 'figure'),
    Input('main-nav-tabs', 'value'),
    Input('year-dropdown', 'value'),
    Input('selected-drivers-store', 'data'),
)
def update_main_figure(tab_id, selected_year, selected_drivers):
    # Flatten the selected_drivers list if needed
    if selected_drivers and isinstance(selected_drivers[0], list):
        selected_drivers = [item for sublist in selected_drivers for item in (sublist if isinstance(sublist, list) else [sublist])]
    
    # Call the visualization function according to tab_id
    if tab_id == 'ranking-evolution':
        return create_ranking_evolution_figure(selected_year, selected_drivers)
    
    elif tab_id == 'driver-instability':
        return create_nvr_figure(selected_year, selected_drivers)

    elif tab_id == 'pace-stability':
        return create_pace_stability_figure(selected_year, selected_drivers, None)
    
    elif tab_id == 'position-flow-stability':
        # For position flow, we need a default driver
        if selected_year:
            df_drivers = data_handler.get_proper_format(selected_year)
            if not df_drivers.empty:
                default_driver = df_drivers['driver_id'].iloc[0]
                df = data_handler.get_position_flow_data(selected_year, default_driver)
                return visualize_position_flow_chart(df)
    
    return go.Figure()

# 5 Update checkbox values when store changes
@app.callback(
    Output({'type': 'driver-checkbox', 'index': ALL}, 'value'),
    Input('selected-drivers-store', 'data'),
    State({'type': 'driver-checkbox', 'index': ALL}, 'id')
)
def update_checkbox_values(selected_drivers, checkbox_ids):
    checkbox_values = []
    for checkbox_id in checkbox_ids:
        driver_id = checkbox_id['index']
        if driver_id in selected_drivers:
            checkbox_values.append([driver_id])
        else:
            checkbox_values.append([])
    return checkbox_values

# 6 Update dropdown container based on tab
@app.callback(
    Output('dynamic-dropdown-container', 'children'),
    Input('main-nav-tabs', 'value'),
    Input('year-dropdown', 'value'),
)
def update_dropdown_container(tab_id, current_year):
    return layouts.get_dropdowns(tab_id, current_year)

# 7 Handle race dropdown changes for Pace Stability
@app.callback(
    Output('main-chart-graph', 'figure', allow_duplicate=True),
    Input('race-dropdown', 'value'),
    State('main-nav-tabs', 'value'),
    State('year-dropdown', 'value'),
    State('selected-drivers-store', 'data'),
    prevent_initial_call=True
)
def update_pace_stability_with_race(selected_race, tab_id, selected_year, selected_drivers):
    if tab_id != 'pace-stability':
        return dash.no_update
    
    return create_pace_stability_figure(selected_year, selected_drivers, selected_race)

# 8 Handle driver dropdown changes for Position Flow Stability
@app.callback(
    Output('main-chart-graph', 'figure', allow_duplicate=True),
    Input('driver-dropdown', 'value'),
    State('main-nav-tabs', 'value'),
    State('year-dropdown', 'value'),
    prevent_initial_call=True
)
def update_position_flow_with_driver(selected_driver, tab_id, selected_year):
    if tab_id != 'position-flow-stability' or not selected_driver:
        return dash.no_update
    
    df = data_handler.get_position_flow_data(selected_year, selected_driver)
    return visualize_position_flow_chart(df)

# 9 Update card values for Position Flow Stability
@app.callback(
    Output('card-points-value', 'children'),
    Input('driver-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_points_card(selected_driver, selected_year):
    if not selected_driver or not selected_year:
        return "-"
    df_driver = data_handler.get_proper_format(selected_year)
    driver_row = df_driver[df_driver['driver_id'] == selected_driver]
    if not driver_row.empty:
        return str(driver_row['total_points'].iloc[0])
    return "-"

@app.callback(
    Output('card-instability-value', 'children'),
    Input('driver-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_instability_card(selected_driver, selected_year):
    if not selected_driver or not selected_year:
        return "-"
    df_inst = data_handler.get_not_valid_race_data(selected_year, [selected_driver])
    if not df_inst.empty:
        nvr = df_inst['nvr'].iloc[0]
        return f"{nvr*100:.0f}%"
    return "-"

@app.callback(
    Output('card-pace-value', 'children'),
    Input('driver-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_pace_card(selected_driver, selected_year):
    if not selected_driver or not selected_year:
        return "-"
    df_pace = data_handler.get_race_pace_data(selected_year, [selected_driver])
    if not df_pace.empty:
        avg_lap = df_pace['lap_time_sec'].mean()
        return f"{avg_lap:.1f} s"
    return "-"

# Run app
if __name__ == '__main__':
    app.run(debug=False, port=8050)
>>>>>>> origin/master
