from app.server import app
from app.config import log, DEBUG
from app.database import Database
from waitress import serve

def main():
    log.info("Initialising Database...")
    db = Database()
    db.initialize()
    db.close()
    log.info("Starting server...")
    if DEBUG:
        app.run(
            debug=True,
            host="0.0.0.0",
            port="8069",
            load_dotenv=False,
        )
    else:
        serve(app, host="0.0.0.0", port="8080")

if __name__ == "__main__":
    main()
