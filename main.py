import asyncio
import logging

import package_logger
import sfdc

def run_main():
    # Initialize logging
    package_logger.initialize_logging()

    logging.info('Starting SFDC Platform Event Monitor.')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sfdc.PlatformEventsClient.start_server())



if __name__ == '__main__':
    run_main()
