from datetime import datetime, timedelta

class Session:
    id: str
    date: str
    title: str

    def __init__(self, db_row:str=None) -> None:
        if db_row is not None:
            if len(db_row) != 3:
                raise ValueError("Unable to unserialize db row in a Session object")
            else:
                self.id = db_row[0]
                self.date = db_row[1]
                self.title = db_row[2]

    @property
    def pretty_date(self) -> str:
        return datetime.fromisoformat(self.date).strftime('%Y-%m-%d, %H:%M')
    
    @property
    def open(self) -> bool:
        return (datetime.fromisoformat(self.date) + timedelta(hours=12)) > datetime.now()