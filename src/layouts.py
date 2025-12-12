from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc 
import pandas as pd
import src.data_handler as data_handler 

<<<<<<< HEAD


=======
>>>>>>> origin/master
# 1 header layout
header_layout = html.Header(
    className='header',
    children=[
        html.Div(className='logo', children=[
            html.Img(
                src="/assets/f1_logo.svg"
            )
        ]),
<<<<<<< HEAD
        #  Nav Tabs
=======
        # Nav Tabs
>>>>>>> origin/master
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
<<<<<<< HEAD
    'RBR': '#405dff',  'MCL': '#f58020',  'FER': '#e12020','MER': '#0bf3d3',
    'AST': '#199972','ALP': '#0093ca','HAA': '#b6babd',
    'RB': '#6592fb','WIL': '#60c4fd','SAU': '#4ce25d',
=======
    'RBR': '#405dff', 'MCL': '#f58020', 'FER': '#e12020', 'MER': '#0bf3d3',
    'AST': '#199972', 'ALP': '#0093ca', 'HAA': '#b6babd',
    'RB': '#6592fb', 'WIL': '#60c4fd', 'SAU': '#4ce25d',
>>>>>>> origin/master
    'AT': '#20394C', 'ARO': '#A42134'
}

# * Create a color map for Driver Selection Table
TEAM_COLORS = {
    'RBR': 'team-rbr', 'MCL': 'team-mcl', 'FER': 'team-fer', 'MER': 'team-mer', 
    'AST': 'team-ast', 'ALP': 'team-alp', 'HAA': 'team-haa', 'RB': 'team-rb2',
    'WIL': 'team-wil', 'SAU': 'team-sau', 'AT': 'team-at', 'ARO': 'team-aro'
}

<<<<<<< HEAD

=======
>>>>>>> origin/master
# 2 Driver Selection Table
# 2.1 Driver Selection Table: table layout
def create_driver_table_rows(df: pd.DataFrame, selected_driver_ids=None):
    # In order to remember those selected between tabs
    if selected_driver_ids is None:
        selected_driver_ids = []
<<<<<<< HEAD
=======
    
>>>>>>> origin/master
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
<<<<<<< HEAD
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
=======
            html.Tr(
                className='driver-row', 
                id={'type': 'driver-row', 'index': driver_id}, 
                children=[
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
                ]
>>>>>>> origin/master
            )
        )
    
    return [html.Table(className='driver-table', children=[header_row, html.Tbody(table_body)])]

<<<<<<< HEAD

=======
>>>>>>> origin/master
# 2.2 Driver Selection Table: table container layout
def create_driver_list_panel(df_drivers: pd.DataFrame, selected_driver_ids):
    # Create right-side layout
    return html.Aside(
        className='driver-list-panel',
        children=[
            html.Div(className='panel-header', children=[
                html.H2('Driver List', className='panel-title'),
            ]),
<<<<<<< HEAD
=======

            # Buttons container
            html.Div([
                # Select All button
                html.Div(
                    [
                        html.Img(
                            src="/assets/select_all.png",
                            className='select-all-button-img',
                            style={'cursor': 'pointer'}
                        ),
                        html.Span('Select All', className='button-text select-all-text'),
                    ],
                    id='select-all-button',
                    className='button-with-text',
                    n_clicks=0,
                ),
                
                # Clear All button
                html.Div(
                    [
                        html.Img(
                            src="/assets/clear_all.png",
                            className='clear-all-button-img',
                            style={'cursor': 'pointer'}
                        ),
                        html.Span('Clear All', className='button-text clear-all-text'),
                    ],
                    id='clear-all-button',
                    className='button-with-text',
                    n_clicks=0,
                )
            ], className='button-container'),
            
            # Horizontal line separator
            html.Hr(className='separator-line'),

            # Driver table
>>>>>>> origin/master
            html.Div(id='dynamic-driver-table-container', children=create_driver_table_rows(df_drivers, selected_driver_ids))
        ]
    )

<<<<<<< HEAD
# 3 Cards: Not Yet Finished!!
=======
# 3 Cards: Summary cards for Position Flow Stability tab
>>>>>>> origin/master
def create_summary_cards():
    # To create right-side cards for Tab 4

    card_types = [ 
        {"key":"points","title": "Season Points","icon":"point_icon"},
        {"key":"instability","title": "Instability","icon":"instab_icon"},
        {"key":"pace","title": "Race Pace","icon":"pace_icon"}
    ]
    cards = []
    for data in card_types:
        value_id = f"card-{data['key']}-value"
        icon_path = f"/assets/{data['icon']}.png"
        icon_img = html.Img(className='card-icon-img',src=icon_path)
        cards.append(
            dbc.Card(
                dbc.CardBody(
                    html.Div(
                        children=[
                            html.H5(children=[data["title"], icon_img], 
                                    className="card-text", 
                                    style={
                                        "fontFamily":"Formula1Font, sans-serif",
                                        "fontSize": "1.1em",
                                        "fontWeight": "500",
                                        "marginBottom":"7px",
                                        "display":"flex",
                                        "justifyContent": "space-between",
                                        "width": "100%"
                                    }
                            ),
                            html.P(id=value_id, 
                                   children=["-"],
                                   className=f"card-text", 
                                   style={"fontSize": "2em",
                                        "fontWeight": "700"}),
                        ],
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
<<<<<<< HEAD
        className='chart-container', children=[
            dcc.Graph(id='main-chart-graph', style={'height': '100%'})  
        ])
=======
        className='chart-container', 
        children=[
            dcc.Graph(id='main-chart-graph', style={'height': '100%'})  
        ]
    )
>>>>>>> origin/master

# 4.3 Combine Top and Down areas
def create_content_area(tab_id, current_year='2024'):
    content_area_top = create_content_area_top(tab_id, current_year)
    content_area_down = create_content_area_down()

    return html.Div(
<<<<<<< HEAD
        className='content-area', children=[
=======
        className='content-area', 
        children=[
>>>>>>> origin/master
            content_area_top,
            content_area_down
        ]
    )
    
# --- Other supporting functions -------

# 1 Define titles according to tab-id
def get_tab_titles(tab_id):
    if tab_id == 'ranking-evolution':
<<<<<<< HEAD
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
    """
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
            style={'width': '150px',"display": "none"}
        )
    )
    """
    # For tab 4, add a driver dropdown button:
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
            style={'width': '200px',"display": "none"}
        )
    )  
        
    return dropdowns

=======
        return "Ranking Point Evolution", "Driver's total points throughout the season"
    elif tab_id == 'driver-instability':
        return "Driver Instability", "Analysis of driver performance variance"
    elif tab_id == 'pace-stability':
        return "Pace Stability", "Driver's lap time consistency analysis"
    elif tab_id == 'position-flow-stability':
        return "Position Flow Stability", "Driver's grid to finish position analysis"
    return "Unknown Tab", ""

def get_dropdowns(tab_id, current_year='2024'):
    race_year = ['2022', '2023', '2024']
    dropdowns = [
        dcc.Dropdown(
            id='year-dropdown', 
            options=[
                {
                    'label': html.Div([
                        html.Span('🗓', style={'marginRight': '10px'}), 
                        html.Span(year)
                    ], style={'display': 'flex', 'alignItems': 'center'}), 
                    'value': year
                } for year in race_year
            ],
            value=current_year,
            clearable=False,
            className='year-dropdown-dash-wrap', 
            style={'width': '150px'} 
        )
    ]


    # Add driver dropdown for Position Flow Stability tab (initially hidden)
    if tab_id == 'position-flow-stability':
        try:
            driver_options = data_handler.get_proper_format(current_year)
            
            dropdowns.append(
                dcc.Dropdown(
                    id='driver-dropdown',
                    options=[
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
                        for _, row in driver_options.iterrows()
                    ],
                    value=driver_options['driver_id'].iloc[0] if not driver_options.empty else None,
                    clearable=False,
                    className='year-dropdown-dash-wrap',
                    style={'width': '200px'}
                )
            )
        except:
            # If there's an error getting driver data, still create the dropdown but empty
            dropdowns.append(
                dcc.Dropdown(
                    id='driver-dropdown',
                    options=[],
                    value=None,
                    clearable=False,
                    className='year-dropdown-dash-wrap',
                    style={'width': '200px'}
                )
            )

    return dropdowns
>>>>>>> origin/master

# --- Ending -------
# Fullpage layout for app.py to render 
full_page_layout = html.Div([
<<<<<<< HEAD
    dcc.Store(id='selected-drivers-store', data=[]), #here
=======
    dcc.Store(id='selected-drivers-store', data=[]),
>>>>>>> origin/master
    header_layout,
    html.Div(id='main-container', 
             className='main-container',
             children=[
        html.Div(id='main-container-left', children=[
            create_content_area('ranking-evolution', current_year='2024')
        ]),
        html.Div(id='main-container-right')
<<<<<<< HEAD
        ]) 
])




=======
    ]) 
])
>>>>>>> origin/master
