# app.py 
import dash
from dash import Input, Output, MATCH, ALL, State, dcc, html, dash_table
from dash import callback_context as ctx
import src.layouts as layouts 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import src.data_handler as data_handler
import src.chart as charts

# Import font 'Inter'
external_stylesheets = [ 
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"
]

# Initialize Dash 
app = dash.Dash(
    __name__, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)

# Dashboard layout
app.layout = layouts.full_page_layout


# ------ callback ----------

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
)
def update_title(tab_id):
    title, subtitle = layouts.get_tab_titles(tab_id) 
    return title, subtitle 

# 2 Render right page (driver selection table, cards)
@app.callback(
    Output('main-container-right', 'children'),
    Input('main-nav-tabs', 'value'),
    Input('year-dropdown', 'value'),
    Input('selected-drivers-store', 'data'),
    
)
def get_sidebar(tab_id, selected_year, stored_drivers):
    # Create right-side content
    
    if tab_id in ['ranking-evolution', 'driver-stability', 'pace-stability']:
        try:
            df_drivers = data_handler.get_proper_format(selected_year)
        except:
            df_drivers = pd.DataFrame({'Team_Code': ['---'], 'Driver_Name': ['---'], 'Points': ['---']})
            
        sidebar = layouts.create_driver_list_panel(df_drivers, stored_drivers)
        
    elif tab_id == 'position-flow-stability':
        sidebar = layouts.create_summary_cards()
        
    else:
        sidebar = html.Div("Not Found")
    
    return sidebar

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
        return [v[0] for v in checkbox_values if v]

# 4 Main chart callback - Simplified version without conditional dropdowns
@app.callback(
    Output('main-chart-graph', 'figure'),
    Input('main-nav-tabs', 'value'),
    Input('year-dropdown', 'value'),
    Input('selected-drivers-store', 'data'),
    Input('driver-dropdown', 'value'),
)
def update_main_figure(tab_id, year, drivers, driver):
    # Flatten the selected_drivers list if needed
    if drivers and isinstance(drivers[0], list):
        drivers = [item for sublist in drivers for item in (sublist if isinstance(sublist, list) else [sublist])]
    
    # Call the visualization function according to tab_id
    if tab_id == 'ranking-evolution':
        return charts.create_ranking_evolution_figure(year, drivers)
    
    elif tab_id == 'driver-stability':
        return charts.create_nvr_figure(year, drivers)

    elif tab_id == 'pace-stability':
        return charts.create_pace_stability_figure(year, drivers)
    
    elif tab_id == 'position-flow-stability':
        if not driver:
            return go.Figure()
        df = data_handler.get_position_flow_data(year, driver)
        return charts.visualize_position_flow_chart(df)
    
    return go.Figure()
""""
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
    return checkbox_values"""

# 6 Update dropdown container based on tab
# try here
@app.callback(
    Output('driver-dropdown', 'style'),
    Input('main-nav-tabs', 'value')
)
def dropdown_toggler(tab_id):
    if tab_id == 'position-flow-stability':
        return {'width': '200px', 'display':'block'}
    else:
        return {'width': '200px', 'display':'None'}



# 4 Update the driver menu
@app.callback(
    Output('driver-dropdown', 'options'),
    Output('driver-dropdown', 'value'),
    [Input('year-dropdown', 'value')]
)
def update_driver_dropdown_options(year):
    if not year:
        return [], None

    df = data_handler.get_proper_format(year)

    options = [
        {
            'label': html.Div([
                html.Span('Driver', style={
                    'fontWeight': '500',
                    'fontSize': '0.9em',
                    'color': "#9f9f9f",
                    'marginRight': '6px'
                }),
                html.Span(row['driver'])
            ], style={'display': 'flex', 'alignItems': 'center'}),
            'value': row['driver_id']
        }
        for _, row in df.iterrows()
    ]

    new_default_value = df['driver_id'].iloc[0] if not df.empty else None
    return options, new_default_value





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
    Output('card-stability-value', 'children'),
    Input('driver-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_stability_card(selected_driver, selected_year):
    if not selected_driver or not selected_year:
        return "-"
    df_stablility = data_handler.get_not_valid_race_data(selected_year, [selected_driver])
    if not df_stablility.empty:
        nvr = df_stablility['nvr'].iloc[0]
        stability = 1-nvr
        return f"{stability*100:.2f}%"
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

@app.callback(
    Output('card-improvement-value', 'children'),
    Input('driver-dropdown', 'value'),
    Input('year-dropdown','value')
)
def update_improvement_card(selected_driver, selected_year):
    if not selected_driver or not selected_year:
        return "-"
    df = data_handler.get_position_flow_data(selected_year, selected_driver)
    if df.empty:
        return "--"
    df = df[
        df["grid_position_text"].notna()
        & df["position_text"].notna()
        & df["grid_position_text"].str.isdigit()
        & df["position_text"].str.isdigit()
    ].copy()

    if df.empty:
        return "--"

    start = df["grid_position_text"].astype(int)
    finish = df["position_text"].astype(int)

    improvement_rate = (finish.le(start).mean()) * 100.0
    return f"{improvement_rate:.0f}%"



# Run app
if __name__ == '__main__':
    app.run(debug=True, port=8050)