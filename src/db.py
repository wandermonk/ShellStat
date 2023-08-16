import os
import sqlite3
import datetime

class TimeseriesDB:
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL") # Set Write-Ahead Logging (WAL) mode.
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        # cerate metrics table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL, -- Date in YYYY-MM-DD format
                            hour INTEGER NOT NULL, -- Hour of the day (0-23)
                            timestamp INTEGER NOT NULL,
                            metric_name TEXT NOT NULL,
                            metric_value REAL NOT NULL,
                            PRIMARY KEY (timestamp, metric_name)
            )
                            ''')
        
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_date_hour ON metrics (date, hour)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_metric_name ON metrics(metric_name)")                     
        
        # create tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            key TEXT NOT NULL,
                            value TEXT NOT NULL,
                            UNIQUE(key, value) -- unique combination of key and value
            )
                            ''')
        
        # create metrics_tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics_tags (
                            metric_id INTEGER NOT NULL,
                            tag_id INTEGER NOT NULL,
                            PRIMARY KEY (metric_id, tag_id),
                            FOREIGN KEY (metric_id) REFERENCES metrics (id),
                            FOREIGN KEY (tag_id) REFERENCES tags (id)
            )
                            ''')
        
        def insert_metric(self, metric_name, metric_value, tags=None):
            now = datetime.now()
            with self.conn:
                self.conn.execute("""
                    INSERT INTO metrics (timestamp, date, hour, metric_name, metric_value, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (now, now.date(), now.hour, metric_name, metric_value, tags))

        def batch_insert_metrics(self, records):
            with self.conn:
                self.conn.executemany("""
                    INSERT INTO metrics (timestamp, date, hour, metric_name, metric_value, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, records)

        def get_metrics(self, metric_name, start_date=None, end_date=None):
                query = "SELECT * FROM metrics WHERE metric_name = ?"
                params = [metric_name]
                
                if start_date:
                    query += " AND date >= ?"
                    params.append(start_date)
                if end_date:
                    query += " AND date <= ?"
                    params.append(end_date)
                
                with self.conn:
                    return self.conn.execute(query, params).fetchall()
                
        def get_metrics_by_tags(self, metric_name, tags):
            query = """
                SELECT * FROM metrics
                INNER JOIN metrics_tags ON metrics.id = metrics_tags.metric_id
                INNER JOIN tags ON metrics_tags.tag_id = tags.id
                WHERE metric_name = ?
                AND tags.key = ?
                AND tags.value = ?
            """
            params = [metric_name]
            params.extend(tags)
            
            with self.conn:
                return self.conn.execute(query, params).fetchall()
        
        def close(self):
            self.conn.close()

def optimized_insertion(db_connection, metric_records):
            db_connection.batch_insert_metrics(metric_records)

def retrieve_metrics(db_connection, metric_name, start_date=None, end_date=None):
    return db_connection.get_metrics(metric_name, start_date, end_date)

def vacuum_database(db_connection):
    with db_connection.conn:
        db_connection.conn.execute("VACUUM")