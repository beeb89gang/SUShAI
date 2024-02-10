
class Order:
    user_id: str
    session_id: str
    order_number: str
    order_name: str
    user_id: str
    user_name: str

    def __init__(self, db_row:str=None) -> None:
        if db_row is not None:
            if len(db_row) != 6:
                raise ValueError("Unable to unserialize db row in a Order object")
            else:
                self.user_id = db_row[0]
                self.session_id = db_row[1]
                self.order_number = db_row[2]
                self.order_name = db_row[3]
                self.user_id = db_row[4]
                self.user_name = db_row[5]

class OrderTotal:
    order_number: str
    order_total: str

    def __init__(self, db_row:str=None) -> None:
        if db_row is not None:
            if len(db_row) != 2:
                raise ValueError("Unable to unserialize db row in a OrderTotal object")
            else:
                self.order_number = db_row[0]
                self.order_total = db_row[1]
