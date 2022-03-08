
from src.monitoring import FinanceApplication


def base_window():
    return FinanceApplication.base_window()


def do_monitoring():
    from config import UPWARD_LIMIT, DOWNWARD_LIMIT
    return FinanceApplication.monitoring(upward_limit=UPWARD_LIMIT, downward_limit=DOWNWARD_LIMIT)


if __name__ == "__main__":
    #my_app = base_window()
    my_app = do_monitoring()
    my_app.run()
