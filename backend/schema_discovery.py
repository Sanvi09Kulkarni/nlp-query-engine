from sqlalchemy import create_engine, inspect

class SchemaDiscovery:
    def analyze_database(self, conn_str: str):
        # For SQLite allow same-thread use
        connect_args = {"check_same_thread": False} if conn_str.startswith("sqlite") else {}
        engine = create_engine(conn_str, connect_args=connect_args, future=True)
        insp = inspect(engine)
        tables = insp.get_table_names()
        schema = {}
        for t in tables:
            cols = insp.get_columns(t)
            schema[t] = {c['name']: str(c.get('type')) for c in cols}
        return schema, engine
