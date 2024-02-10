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
