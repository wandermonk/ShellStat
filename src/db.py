import sqlite3
from datetime import datetime

class TimeseriesDB:
    def __init__(self, db_name="metrics.db"):
        try:
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode=WAL") # Set Write-Ahead Logging (WAL) mode.
            result = self.conn.execute("PRAGMA journal_mode").fetchone()[0]
            if result != "wal":
                raise ValueError("Unable to set WAL mode")
            print(f"Journal mode: {result}")
            self.cursor = self.conn.cursor()
            self._create_tables()
            self.buffer = []
        except Exception as e:
            print(f"Error connecting to database {db_name}")
            print(e)
    
    def _create_tables(self):
        # create metadata table for metrics table
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS metrics_table_metadata (
                        table_name TEXT NOT NULL,
                        granularity TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL
                    )
                        ''')
        # create tags table for metrics table
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tags (
                            id INTEGER PRIMARY KEY,
                            key TEXT NOT NULL,
                            value TEXT NOT NULL,
                            UNIQUE(key, value)
                    )
                            ''')
        self.conn.commit()

    def _create_metrics_partition_table(self, table_name):
        self.conn.execute(f'''
                        CREATE TABLE IF NOT EXISTS {table_name} (
                            id INTEGER AUTO_INCREMENT,
                            timestamp TEXT NOT NULL,
                            metric_name TEXT NOT NULL,
                            metric_value REAL NOT NULL,
                            PRIMARY KEY (timestamp, metric_name)
                        )
                              ''')
        self.conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_metric_name ON {table_name}(metric_name)")
        # create metric_tags table for this partition
        self.conn.execute(f'''
                        CREATE TABLE IF NOT EXISTS {table_name}_tags (
                            metric_id INTEGER NOT NULL,
                            tag_id INTEGER NOT NULL,
                            PRIMARY KEY (metric_id, tag_id),
                            FOREIGN KEY (metric_id) REFERENCES {table_name}(id),
                            FOREIGN KEY (tag_id) REFERENCES tags(id)
                        )
                              ''')  
        self.conn.commit()

    def _get_relevant_partitions(self, granularity, start_time, end_time):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT table_name FROM metrics_table_metadata
            WHERE granularity=? AND start_time<=? AND end_time>=?
        """, (granularity, start_time, end_time))
        return [row[0] for row in cur.fetchall()]
    
    def _construct_union_query(self, table_names, metric_name, start_time, end_time):
        queries = []
        for table in table_names:
            queries.append(f"""
                        SELECT timestamp, metric_name, metric_value, tags FROM {table}
                        WHERE metric_name=? AND timestamp>=? AND timestamp<=?
                        """, (metric_name, start_time, end_time))
        return " UNION ".join(queries)
    
    # maintaining microsecond time precision in writes.
    def insert_metric(self, metric_name, metric_value, tags=None):
        now=datetime.now()
        table_name=f"metrics_{now.strftime('%Y_%m_%d')}"
        print(f"Inserting metric {metric_name} with value {metric_value} into table {table_name}")
        
        # check if the partition table exists
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM metrics_table_metadata WHERE table_name=?", (table_name,))
        exists = cur.fetchone()
        print(f"Table {table_name} exists: {exists}")
        if not exists:
            self._create_metrics_partition_table(table_name)
            self.conn.execute("""
                    INSERT INTO metrics_table_metadata (table_name, granularity, start_time, end_time)
                    VALUES (?, ?, ?, ?)
            """, (table_name, "hourly", f"{now.date()} {now.hour}:00:00", f"{now.date()} {now.hour}:59:59"))   
        
        cur.execute(f"""
                        INSERT INTO {table_name} (timestamp, metric_name, metric_value)
                        VALUES (?, ?, ?)
                        """, (now.strftime('%Y-%m-%d %H:%M:%S.%f'), metric_name, metric_value))
        
        metric_id = cur.lastrowid

        # insert tags into tags table
        if tags:
            for tag in tags:
                # check if tag exists or insert it
                cur.execute("INSERT OR IGNORE INTO tags (key, value) VALUES (?, ?)", (tag['key'], tag['value']))
                cur.execute("SELECT id FROM tags WHERE key=? AND value=?", (tag['key'], tag['value']))
                tag_id = cur.fetchone()[0]
                # Map metric to tag
                cur.execute(f"INSERT INTO {table_name}_tags (metric_id, tag_id) VALUES (?, ?)", (metric_id, tag_id))
        self.conn.commit()

    def query_metric(self, granularity, metrics_name, start_time, end_time):
        partitions = self._get_relevant_partitions(granularity, start_time, end_time)
        if not partitions:
            return []
        query = self._construct_union_query(partitions, metrics_name, start_time, end_time)
        cur = self.conn.cursor()
        cur.execute(query, (metrics_name, start_time, end_time) * len(partitions))
        return cur.fetchall()

    def get_metrics_metadata(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM metrics_table_metadata")
        return cur.fetchall()
    
    def close(self):
        self.conn.close()
        
