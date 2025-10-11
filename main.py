from api import createapp
from flask_sqlalchemy import SQLAlchemy
import os
import logging 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = createapp()

db_path = os.path.join(os.path.dirname(__file__), 'cache.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def main():
    print("Hello from league-hackathon!")
    app.run(debug=True)


if __name__ == "__main__":
    main()
