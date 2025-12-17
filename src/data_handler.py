import pandas as pd
import sqlite3
import os
import numpy as np

# 1. Database Path - using relative paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH_1 = os.path.join(BASE_DIR, 'data', 'f1_1.db')


# for db1
def query_db(sql, args=(), one=False):
    """Execute a read-only query and return rows as dict-like objects."""
    conn = sqlite3.connect(DB_PATH_1)   
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

# 1. Driver Selection Table
# 1.1 Driver Selection Table: formatting 
def get_proper_format(selected_year):
    constructor_map = {
        "aston-martin": "AST", "alpine": "ALP",
        "haas": "HAA", "alphatauri": "AT",
        "alfa-romeo": "ARO", "williams": "WIL",
        "kick-sauber": "SAU", "rb": "RB"
    }
    df = get_current_season_drivers(selected_year)
    df["team"] = df["constructor_id"].map(constructor_map)
    df["driver"] = df["driver_id"].str.split("-").str[-1].str.capitalize()
    return df

# 1.2 Driver Selection Table: data
def get_current_season_drivers(selected_year):
    query = """
    SELECT year, constructor_id, driver_id, total_points
    FROM (
        SELECT sd.year, sed.constructor_id, sd.driver_id, sd.total_points,
        ROW_NUMBER() OVER (
        PARTITION BY sd.year
        ORDER BY sd.total_points DESC
        ) AS rn
        FROM season_driver sd
        JOIN season_entrant_driver sed
        ON sd.year = sed.year
        AND sd.driver_id = sed.driver_id
        WHERE sd.year IN ('2022', '2023', '2024')
        AND sed.constructor_id NOT IN ('mclaren', 'red-bull', 'ferrari', 'mercedes')
    )
    WHERE rn <= 12 AND year = ?
    ORDER BY year DESC, total_points DESC;
    """
    rows = query_db(query, (selected_year,))
    df = pd.DataFrame(rows, columns=["year", "constructor_id", "driver_id", "total_points"])
    return df

# 2 Ranking Evolution: data
def get_ranking_evolution_data(selected_year, selected_drivers):
    if not selected_drivers:
        return pd.DataFrame()
    
    placeholders = ",".join(["?"] * len(selected_drivers))
    query = f"""
        SELECT
            race.id,
            race_driver_standing.driver_id,
            race.year,
            race.round,
            race.official_name,
            race_driver_standing.points,
            constructor.id AS constructor_id
        FROM race_driver_standing
        JOIN race
            ON race.id = race_driver_standing.race_id
        JOIN season_entrant_driver 
            ON season_entrant_driver.driver_id = race_driver_standing.driver_id 
           AND season_entrant_driver.year = race.year
        JOIN constructor
            ON constructor.id = season_entrant_driver.constructor_id
        WHERE race.year = ?
          AND race_driver_standing.driver_id IN ({placeholders})
        ORDER BY race.round;
    """
    params = tuple([selected_year] + selected_drivers)
    rows = query_db(query, params)
    df = pd.DataFrame(rows, columns=["race_id", "driver_id", "year", "round", 'official_name', 'points', 'constructor_id'])
    
    constructor_map = {
        "aston-martin": "AST", "alpine": "ALP",
        "haas": "HAA", "alphatauri": "AT",
        "alfa-romeo": "ARO", "williams": "WIL",
        "kick-sauber": "SAU", "rb": "RB"
    }
    df["team"] = df["constructor_id"].map(constructor_map)
    return df

# 3 Driver stability: data
def get_not_valid_race_data(selected_year, selected_drivers):
    if not selected_drivers:
        return pd.DataFrame()
    
    driver_placeholders = ', '.join(['?'] * len(selected_drivers))
    query = f"""
    SELECT r.year, d.last_name AS "driver", d.name AS "fullname",
    COUNT(rr.race_id) AS "total_race_count",
    COUNT(CASE WHEN rr.position_number IS NOT NULL THEN 1 ELSE NULL END) AS "total_finished_race_count", 
    COUNT(CASE WHEN rr.position_text IN ('DNF','DNS','DNQ','DSQ','NC') THEN 1 ELSE NULL END) AS "dnf_count",
    rr.constructor_id
    FROM race_result AS rr
    JOIN race AS r ON rr.race_id = r.id
    JOIN driver AS d ON rr.driver_id = d.id
    WHERE r.year = ?
    AND rr.driver_id IN ({driver_placeholders})
    AND rr.constructor_id NOT IN ('mclaren', 'red-bull', 'ferrari', 'mercedes')
    GROUP BY r.year, d.name, rr.constructor_id
    """
    params = tuple([selected_year] + selected_drivers)

    rows = query_db(query, params)
    df = pd.DataFrame(rows, columns=['year', 'driver', 'fullname', 'total_race_count', 'total_finished_race_count', 'dnf_count', 'constructor_id'])
    
    # Calculate Not Valid Race percentage
    df['nvr'] = df.apply(
        lambda row: row['dnf_count'] / row['total_race_count'] if row['total_race_count'] > 0 else 0,
        axis=1
    )
    
    constructor_map = {
        "aston-martin": "AST", "alpine": "ALP",
        "haas": "HAA", "alphatauri": "AT",
        "alfa-romeo": "ARO", "williams": "WIL",
        "kick-sauber": "SAU", "rb": "RB"
    }
    df["team"] = df["constructor_id"].map(constructor_map)
    return df

# 4 Pace Stability: data
def get_race_pace_data(selected_year, selected_drivers=None, selected_race=None):
    """
    Fetch race pace per lap data for the selected year and drivers.
    """
    if selected_drivers is None or len(selected_drivers) == 0:
        return pd.DataFrame()
    
    driver_placeholders = ','.join(['?'] * len(selected_drivers))
    
    # Build the query based on whether a specific race is selected
    if selected_race:
        query = f"""
        SELECT 
            r.year, 
            d.name,
            d.abbreviation AS driver,  
            rr.race_id, r.grand_prix_id, 
            rr.position_text, rr."time", rr.time_millis, rr.laps, r.course_length, 
            rr.time_millis/(rr.laps) AS race_pace_per_lap_millis,
            rr.constructor_id
        FROM race_result AS rr
        JOIN race AS r ON rr.race_id = r.id
        JOIN driver AS d ON rr.driver_id = d.id
        WHERE r.year = ?
        AND rr.driver_id IN ({driver_placeholders})
        AND r.name = ?
        AND rr.position_text NOT IN ('DNF', 'DNS', 'DNQ', 'DSQ')
        ORDER BY d.abbreviation, rr.race_id
        """
        params = tuple([selected_year] + selected_drivers + [selected_race])
    else:
        query = f"""
        SELECT 
            r.year, 
            d.name,
            d.last_name AS driver,
            d.abbreviation,  
            rr.race_id, r.grand_prix_id, 
            rr.position_text, rr."time", rr.time_millis, rr.laps, r.course_length, 
            rr.time_millis/(rr.laps) AS race_pace_per_lap_millis,
            rr.constructor_id
        FROM race_result AS rr
        JOIN race AS r ON rr.race_id = r.id
        JOIN driver AS d ON rr.driver_id = d.id
        WHERE r.year = ?
        AND rr.driver_id IN ({driver_placeholders})
        AND rr.position_text NOT IN ('DNF', 'DNS', 'DNQ', 'DSQ')
        ORDER BY d.abbreviation, rr.race_id
        """
        params = tuple([selected_year] + selected_drivers)
    
    rows = query_db(query, params)
    
    df = pd.DataFrame(rows, columns=[
        "year", "name", "driver", "driver_code", "race_id", "grand_prix_id", 
        "position_text", "time", "time_millis", "laps", "course_length", 
        "race_pace_per_lap_millis", "constructor_id"  
    ])
    
    if df.empty:
        return df
    
    # Convert milliseconds to seconds
    df['lap_time_sec'] = df['race_pace_per_lap_millis'] / 1000

    # Map constructor_id to team code
    constructor_map = {
        "aston-martin": "AST", "alpine": "ALP",
        "haas": "HAA", "alphatauri": "AT",
        "alfa-romeo": "ARO", "williams": "WIL",
        "kick-sauber": "SAU", "rb": "RB"
    }
    df["team"] = df["constructor_id"].map(constructor_map)
    
    return df

def remove_outliers_from_pace_data(df):
    """
    Remove outliers from pace data using IQR method.
    Groups by driver and removes values outside 1.5 * IQR.
    """
    if df.empty:
        return df
    
    def remove_outlier(group):
        Q1 = group['lap_time_sec'].quantile(0.25)
        Q3 = group['lap_time_sec'].quantile(0.75)
        IQR = Q3 - Q1
        return group[
            (group['lap_time_sec'] >= Q1 - 1.5 * IQR) &
            (group['lap_time_sec'] <= Q3 + 1.5 * IQR)
        ]
    
    return df.groupby("driver", group_keys=False).apply(remove_outlier)

# 5 Position Flow Stability: data
def get_position_flow_data(selected_year, selected_driver_id):
    if not selected_driver_id:
        return pd.DataFrame()
    
    
    with sqlite3.connect(DB_PATH_1) as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(race_result)")
        columns = cur.fetchall()
    
    query = f"""
        SELECT
            r.year,
            d.name AS driver_name,
            d.last_name AS driver,
            rr.grid_position_text AS grid_position_text,
            rr.position_text AS position_text
        FROM race_result AS rr
        JOIN race r ON rr.race_id = r.id
        JOIN driver d ON rr.driver_id = d.id
        JOIN constructor c ON rr.constructor_id = c.id
        WHERE r.year = ?
          AND rr.driver_id = ?
          AND rr.position_text NOT IN ('DNF','DNS','DNQ','DSQ','NC')
        ORDER BY r.date;
    """
    with sqlite3.connect(DB_PATH_1) as conn:
        df = pd.read_sql_query(query, conn, params=(selected_year, selected_driver_id))
    
    return df