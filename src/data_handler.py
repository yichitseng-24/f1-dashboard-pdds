import pandas as pd
import sqlite3
import os

# 1. Database Path 
#  data_handler.py in src/ file.
# we os.path.join to get relative path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH_1 = os.path.join(BASE_DIR, 'data', 'f1_1.db')
DB_PATH_2 = os.path.join(BASE_DIR, 'data', 'f1_2.db')

# for db1
def query_db(sql, args=(), one=False):
    """Execute a read-only query and return rows as dict-like objects."""
    conn = sqlite3.connect(DB_PATH_1)   
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

# for db2
def query_db2(sql, args=(), one=False):
    """Execute a read-only query and return rows as dict-like objects."""
    conn = sqlite3.connect(DB_PATH_2)   
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, args)
    rows = cur.fetchall()
    conn.close()
    return (rows[0] if rows else None) if one else rows

# 1. Driver Selection Table
# 1.1 Driver Selection Table: formatting 
# (1) aston-martin -> AST (2) lando-norris -> Lando
def get_proper_format(selected_year):
     constructor_map = {
          "aston-martin": "AST", "alpine": "ALP",
          "haas": "HAA", "alphatauri": "AT",
          "alfa-romeo":"ARO","williams":"WIL",
          "kick-sauber":"SAU","rb":"RB"
          }
     df = get_current_season_drivers(selected_year)
     df["team"] = df["constructor_id"].map(constructor_map)
     df["driver"] = df["driver_id"].str.split("-").str[-1].str.capitalize()
     return df
#1.2 Driver Selection Table: data
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
        WHERE rn <= 12  AND year = ?
        ORDER BY year DESC, total_points DESC;
        """
       rows=query_db(query, (selected_year,))
       df=pd.DataFrame(rows, columns=["year","constructor_id","driver_id", "total_points"])
       return df


# 2 Ranking Evolution : data
def get_ranking_evolution_data(selected_year, selected_drivers):
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
    rows=query_db(query, params)
    df=pd.DataFrame(rows, columns=["race_id","driver_id","year", "round", 'official_name', 'points', 'constructor_id'])
    constructor_map = {
          "aston-martin": "AST", "alpine": "ALP",
          "haas": "HAA", "alphatauri": "AT",
          "alfa-romeo":"ARO","williams":"WIL",
          "kick-sauber":"SAU","rb":"RB"
          }
    df["team"] = df["constructor_id"].map(constructor_map)
    return df

# 2 Driver Instability: data
def get_not_valid_race_data(selected_year, selected_drivers):
       driver_placeholders = ', '.join(['?'] * len(selected_drivers))
       query = f"""
       SELECT r.year, d.last_name AS "driver", d.name AS "fullname",
       COUNT(rr.race_id) AS "total_race_count",
       COUNT (CASE WHEN rr.position_number IS NOT NULL THEN 1 ELSE NULL END) AS "total_finished_race_count", 
       COUNT(CASE WHEN rr.position_text IN ('DNF','DNS','DNQ','DSQ','NC') THEN 1 ELSE NULL END) AS "dnf_count",
       rr.constructor_id
       FROM race_result AS rr
       JOIN race AS r ON rr.race_id = r.id
       JOIN driver AS d ON rr.driver_id = d.id
       WHERE r.year = ?
       AND rr.driver_id IN ({driver_placeholders})
       --IN ('2022', '2023', '2024')
       GROUP BY r.year, d.name
       """
       params = tuple([selected_year]+selected_drivers)

       rows=query_db(query, params)
       df=pd.DataFrame(rows, columns=['year', 'driver','fullname','total_race_count' ,'total_finished_race_count', 'dnf_count','constructor_id'])
       df['nvr'] = df['dnf_count']/df['total_finished_race_count']
       constructor_map = {
          "aston-martin": "AST", "alpine": "ALP",
          "haas": "HAA", "alphatauri": "AT",
          "alfa-romeo":"ARO","williams":"WIL",
          "kick-sauber":"SAU","rb":"RB"
          }
       df["team"] = df["constructor_id"].map(constructor_map)
       return df
print(get_not_valid_race_data(2024, ['lance-stroll']))

# 3 Pace Stability: data
# input year : value
# input driver: a list
"""stella's code"""



# 4 Position Flow Stability: data
"""lam's code"""



# 5 Cards: data

# 6 year-dropdown option: data

# 7 GP-dropdown option: data
