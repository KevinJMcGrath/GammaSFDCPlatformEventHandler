from server import async_manager as am
import package_logger


def run_main():
    # Initialize logging
    package_logger.initialize_logging()
    am.start_server()

if __name__ == '__main__':
    run_main()
