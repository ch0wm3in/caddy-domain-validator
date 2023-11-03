import logging

from quart import Quart, request, jsonify
from watchdog.observers import Observer

from handler import HostnameChangeHandler

logging.basicConfig(level=logging.INFO)
app = Quart(__name__)

event_handler = HostnameChangeHandler()
observer = Observer()
observer.schedule(event_handler, event_handler.monitored_directory, recursive=False)
observer.start()

app.logger.info(f'Permitted domains: {" ".join(event_handler.scan_hostnames())}')


def check_domain(domain: str) -> bool:
    sampled = '.'.join(domain.split('.')[-2:])
    return sampled in event_handler.valid_hostnames


@app.route('/validate', methods=['GET'])
def main():
    domain = request.args.get('domain')
    if check_domain(domain):
        return jsonify({'message': f'Domain {domain} is valid'}), 200
    else:
        return jsonify({'message': f'Domain {domain} is not valid'}), 403
