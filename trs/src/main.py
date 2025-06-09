from src.config import settings
from src.stream import StreamService


def main():
    StreamService(settings.FLOW).process()


if __name__ == "__main__":
    main()
