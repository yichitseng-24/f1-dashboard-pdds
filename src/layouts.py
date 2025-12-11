from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc 
import pandas as pd
import src.data_handler as data_handler 

# 1 header layout
header_layout = html.Header(
    className='header',
    children=[
        html.Div(className='logo', children=[
            html.Img(
                src="/assets/f1_logo.svg"
            )
        ]),
        #  Nav Tabs
        dcc.Tabs(
            id='main-nav-tabs',
            value='ranking-evolution',
            parent_className='nav-tabs',
            className='nav-tabs-container',       
            children=[
                dcc.Tab(label='Ranking Point Evolution', value='ranking-evolution', className='nav-tab', selected_className='nav-tab--selected'),
                dcc.Tab(label='Driver Instability', value='driver-instability', className='nav-tab', selected_className='nav-tab--selected'),
                dcc.Tab(label='Pace Stability', value='pace-stability', className='nav-tab', selected_className='nav-tab--selected'),
                dcc.Tab(label='Position Flow Stability', value='position-flow-stability', className='nav-tab', selected_className='nav-tab--selected'),
            ]
        ),
    ]
)

# * Create a color map for Plotly 
PLOTLY_TEAM_COLOR_MAP = {
    'RBR': '#405dff',  'MCL': '#f58020',  'FER': '#e12020','MER': '#0bf3d3',
    'AST': '#199972','ALP': '#0093ca','HAA': '#b6babd',
    'RB': '#6592fb','WIL': '#60c4fd','SAU': '#4ce25d',
    'AT': '#20394C', 'ARO': '#A42134'
}

# * Create a color map for Driver Selection Table
TEAM_COLORS = {
    'RBR': 'team-rbr', 'MCL': 'team-mcl', 'FER': 'team-fer', 'MER': 'team-mer', 
    'AST': 'team-ast', 'ALP': 'team-alp', 'HAA': 'team-haa', 'RB': 'team-rb2',
    'WIL': 'team-wil', 'SAU': 'team-sau', 'AT': 'team-at', 'ARO': 'team-aro'
}


# 2 Driver Selection Table
# 2.1 Driver Selection Table: table layout
def create_driver_table_rows(df: pd.DataFrame, selected_driver_ids=None):
    # In order to remember those selected between tabs
    if selected_driver_ids is None:
        selected_driver_ids = []
    header_row = html.Thead(children=[
        html.Tr(children=[
            html.Th(style={'width': '40px'}), 
            html.Th("TEAM", className='driver-table-header'),
            html.Th("DRIVER", className='driver-table-header'),
            html.Th("POINTS", className='driver-table-header', style={'textAlign': 'right'}),
        ])
    ])
    
    table_body = []
    
    for index, row in df.iterrows(): 
        driver_id = row['driver_id']
        team_class = TEAM_COLORS.get(row['team'], '')

        if selected_driver_ids:
            value = [driver_id] if driver_id in selected_driver_ids else []
        else:
            value = [driver_id] if index < 12 else []
        
        table_body.append(
            # 使用模式匹配 ID 來實現 Callbacks
            html.Tr(className='driver-row', id={'type': 'driver-row', 'index': driver_id}, children=[
                html.Td(className='checkbox-cell', children=[
                    dcc.Checklist(
                        id={'type': 'driver-checkbox', 'index': driver_id},
                        options=[{'label': '', 'value': driver_id}],
                        value=value,
                        inline=True,
                        className='driver-checkbox',
                    )
                ]),
                html.Td(row['team'], className=f'team-cell {team_class}'),
                html.Td(row['driver'], className='driver-cell'),
                html.Td(row['total_points'], className='points-cell'),
            ], 
            #style={'backgroundColor': '#f0f8ff'} if index < 4 else {} #default selected bg color 
            )
        )
    
    return [html.Table(className='driver-table', children=[header_row, html.Tbody(table_body)])]


# 2.2 Driver Selection Table: table container layout
def create_driver_list_panel(df_drivers: pd.DataFrame, selected_driver_ids):
    # Create right-side layout
    return html.Aside(
        className='driver-list-panel',
        children=[
            html.Div(className='panel-header', children=[
                html.H2('Driver List', className='panel-title'),
            ]),
            html.Div(id='dynamic-driver-table-container', children=create_driver_table_rows(df_drivers, selected_driver_ids))
        ]
    )

# 3 Cards: Not Yet Finished!!
def create_summary_cards():
    # To create right-side cards for Tab 4
    # 要有一個driver, year變數來裝現在選到的資料
    # 傳入抓data的功能或是用現在已經有的數據來做
    # Card: real data should be from data_handler.py
    card_data = [ 
        {"title": "Season Points", "value": "95%", "color": "success"},
        {"title": "Instability", "value": "12 pts", "color": "warning"},
        {"title": "Race Pace", "value": "上升", "color": "primary"},
    ]
    cards = []
    for data in card_data:
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    html.Div(
                        children=[
                            html.H5(data["title"], 
                                    className="card-text", 
                                    style={
                                        "fontSize": "1.4em",
                                        "fontWeight": "700",
                                        "marginBottom":"7px"
                                    }
                            ),
                            html.P(data["value"], className=f"card-text text-{data['color']}", style={"fontSize": "2em",
                                        "fontWeight": "700"}),
                        ],
                        
                        #style={
                        #     "display": "flex",
                        #     "justifyContent": "space-between",
                        #     "alignItems": "center",
                        #     "width": "100%"
                        #}
                        
                    )
                ),
                className='driver-summary-card',
                style={
                    "textAlign": "left",
                    "marginBottom": "25px"
                }
            )
        )
        
    return html.Aside(
        id='tab-4-sidebar',
        #className='driver-list-panel', # 沿用之前的側邊欄容器樣式
        children=html.Div(cards, style={"padding": "10px"})
    )

# 4 Right-side content
# 4.1 Right-side content : Top (Title + Dropdowns)
def create_content_area_top(tab_id, current_year):
    """根據選中的 Tab ID 渲染不同的內容佈局"""
    # get dynamic titles
    title, subtitle = get_tab_titles(tab_id) 

    return html.Div(
        id='content-area-top',
        style={
            'display': 'flex',        
            'justifyContent': 'space-between', 
            'alignItems': 'flex-start',   
            'marginBottom': '3px'    
        },
        children=[
            # A. Title and Subtitle (left)
            html.Div(className='page-header', children=[
                html.H1(id='page-title-h1', children=title, className='page-title'),
                html.P(id='page-subtitle-p', children=subtitle, className='page-subtitle'),
            ]),

            # B. Dropdowns filters (right)
            html.Div(
                id='dynamic-dropdown-container',
                className='year-selector', 
                children=get_dropdowns(tab_id, current_year)
            )
        ]
    )

# 4.2 Right-side content : Down (main chart)
def create_content_area_down():
    return html.Div(
        id='content_area_down',
        className='chart-container', children=[
            dcc.Graph(id='main-chart-graph', style={'height': '100%'})  
        ])

# 4.3 Combine Top and Down areas
def create_content_area(tab_id, current_year='2024'):
    content_area_top = create_content_area_top(tab_id, current_year)
    content_area_down = create_content_area_down()

    return html.Div(
        className='content-area', children=[
            content_area_top,
            content_area_down
        ]
    )
    
# --- Other supporting functions -------

# 1 Define titles according to tab-id
def get_tab_titles(tab_id):
    if tab_id == 'ranking-evolution':
        return "Ranking Point Evolution", "Driver's total points about throughout the season"
    elif tab_id == 'driver-instability':
        return "Driver Instability", "Analysis of driver performance variance."
    elif tab_id == 'pace-stability':
        return "Pace Stability", "Driver's pace stability just ask gpt"
    elif tab_id == 'position-flow-stability':
        return "Position Flow Stability", "Driver ‘s performance about throughout the season"
    return "Unknown Tab", ""

# 2 Define dropdowns elements according to tab-id
def get_dropdowns(tab_id, current_year='2024'):

    race_year = ['2022', '2023', '2024']
    dropdowns=[
        dcc.Dropdown(
            id='year-dropdown', 
            options=[
                {'label':
                 #'🗓'+' '+f'  {y}', 'value': y} for y in ['2022', '2023', '2024']
                    html.Div([
                        html.Span('🗓', style={'marginRight': '10px'}), 
                        html.Span(year)], style={'display': 'flex', 'alignItems': 'center'}), 
                'value': year} for year in race_year
                ],
                value=current_year,
                clearable=False,
                className='year-dropdown-dash-wrap', 
                style={'width': '150px'} 
                )
    ]

    # For tab 3, add a race dropdown button
    
    if tab_id == 'pace-stability':
        # Here we need a function to access a race options according to current_year
        race_options =['Japan', 'Qatar'] 
        dropdowns.append(
            dcc.Dropdown(
                id='race-dropdown', 
                options=[
                    {'label': html.Div([
                        # Style "GP" 
                        html.Span('GP', style={
                            'fontWeight': '500',      
                            'fontSize': '0.9em',      
                            'color': "#9f9f9f",     
                            'marginRight': '6px'      
                        }), 
                        
                        html.Span(race_name)
                        
                    ], style={'display': 'flex', 'alignItems': 'center'}), 
                    
                    'value': race_name} 
                    
                    for race_name in race_options
                ],
                value='Japan',
                clearable=False,
                className='year-dropdown-dash-wrap', 
                style={'width': '150px'}
                )
        )

    # For tab 4, add a driver dropdown button:

    if tab_id == 'position-flow-stability':
        # Get drivers every year as options : Need to debug -- driver options don't change as current_year
        driver_options = data_handler.get_proper_format(current_year)['driver'].tolist()
        #driver_options =['Albon', 'Alonso']
        dropdowns.append(
            dcc.Dropdown(
                id='driver-dropdown', 
                options=[
                    {'label': html.Div([
                        html.Span('Driver', style={
                            'fontWeight': '500',     
                            'fontSize': '0.9em',      
                            'color': "#9f9f9f",     
                            'marginRight': '6px'      
                        }), 
                        #html.Span(current_year),
                        html.Span(driver)
                        
                    ], style={'display': 'flex', 'alignItems': 'center'}), 
                    
                    'value': driver} 
                    
                    for driver in driver_options
                ],
                value='Alonso',
                clearable=False,
                className='year-dropdown-dash-wrap', 
                style={'width': '200px'}
                )
        )
    return dropdowns



# --- Ending -------
# Fullpage layout for app.py to render 
full_page_layout = html.Div([
    dcc.Store(id='selected-drivers-store', data=[]), #here
    header_layout,
    html.Div(id='main-container', 
             className='main-container',
             children=[
        html.Div(id='main-container-left', children=[
            create_content_area('ranking-evolution', current_year='2024')
        ]),
        html.Div(id='main-container-right')
        ]) 
])




