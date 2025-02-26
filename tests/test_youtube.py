from dotenv import load_dotenv
from src.youtube import get_subscriptions

load_dotenv()

if __name__ == "__main__":
    subscriptions = get_subscriptions()
    print(subscriptions)
