from api import createapp
import logging 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = createapp()

def main():
    print("Hello from league-hackathon!")
    app.run(debug=True)


if __name__ == "__main__":
    main()
