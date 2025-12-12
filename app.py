# app.py 
import dash
from dash import Input, Output, ALL, State, dcc, html,  no_update
import src.layouts as layouts 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import src.data_handler as data_handler 


# Import font 'Inter'
external_stylesheets = [ 
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"
]

# Initialize Dash 
# Dash 會自動尋找並載入 assets/f1_styles.css
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True # 啟用這項以支援 Tab 切換時的動態內容
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
        team_color = layouts.PLOTLY_TEAM_COLOR_MAP.get(team, "#808080") # 使用灰色作為默認顏色
        fig.add_trace(
            go.Scatter(
                x=sub["round"],
                y=sub["points"],
                mode="lines+markers",
                name=f"{driver} ({team})",  
                legendgroup=team,
                line=dict(color=team_color),
                hovertemplate=
                    #"<span style='color:" + team_color + "'><b>%{text}</b></span><br>" +
                    driver_name + "<br>" + #may be a bug
                    "Team: " + team + "<br>" +
                    "Round: %{x}<br>" +
                    "Points: %{y}<br>" +
                    "<extra></extra>"
            )
        )
    year_value = df["year"].iloc[0]
    fig.update_layout(
        xaxis_title="Round",
        yaxis_title="Points",
        legend_title="Driver",
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(
            tickmode='linear',
            #dtick=1
        ),
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
    try:
        df = data_handler.get_not_valid_race_data(selected_year, selected_drivers)
    except Exception:
        return fig
    
    if df.empty:
        return fig
    
    df_sorted = df.sort_values(by='nvr', ascending=False)
    current_drivers = df_sorted['driver'].tolist()
    
    fig = px.bar(df, x='driver', y='nvr', 
                 color='team', color_discrete_map=layouts.PLOTLY_TEAM_COLOR_MAP,
                 template='simple_white'
    )
    fig.update_layout(
        hoverlabel=dict(
            font=dict(
                size=14
            )
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )
    fig.update_xaxes(
        title_text='',
        categoryorder='array',
        categoryarray=current_drivers
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
"""def (selected_year, selected_driver)
return fig
"""

# ------ callback ----------

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
)
def update_title(tab_id):
    title, subtitle = layouts.get_tab_titles(tab_id) 
    return title, subtitle 


# 2 Render right page (driver selection table, cards)
@app.callback(
        Output('main-container-right', 'children'),
        [
            Input('main-nav-tabs', 'value'),
            Input('year-dropdown', 'value'),
            Input('selected-drivers-store', 'data')
        ]
)
def get_sidebar(tab_id, selected_year, stored_drivers):
    # Create right-side content
    
    if tab_id in ['ranking-evolution', 'driver-instability', 'pace-stability']:
        # For the first three tabs, show dynamic driver selection table
        try:
            df_drivers = data_handler.get_proper_format(selected_year)
        except:
            df_drivers = pd.DataFrame({'Team_Code': ['---'], 'Driver_Name': ['---'], 'Points': ['---']})
            
        sidebar = layouts.create_driver_list_panel(df_drivers, stored_drivers)
        
    elif tab_id == 'position-flow-stability':
        # For tab 4, show information cards: Not Yet Finished
        sidebar = layouts.create_summary_cards()
        
    else:
        # In case of error
        sidebar = html.Div("Not Found")
    
    return sidebar


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
    driver_options = data_handler.get_proper_format(year)['driver'].tolist()
    options=[
        {'label': html.Div([
            html.Span('Driver', 
                      style={
                          'fontWeight': '500', 'fontSize': '0.9em','color': "#9f9f9f",'marginRight': '6px'
                          }),
                    html.Span(driver)
                    ], style={'display': 'flex', 'alignItems': 'center'}), 
                    'value': driver} 
                    for driver in driver_options
    ]
    new_default_value = driver_options[0] if driver_options else None
    return options, new_default_value


# 4 Update main chart
# According to tab_id and selected_year, selected_drivers
@app.callback(
        Output('main-chart-graph', 'figure'),
        [
        Input('main-nav-tabs', 'value'),
        Input('year-dropdown', 'value'),
        Input({'type': 'driver-checkbox', 'index': ALL}, 'value') 
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
        Input('driver-dropdown','value'),
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

