from quart import Quart, request, jsonify
from watchdog.observers import Observer

from handler import HostnameChangeHandler

app = Quart(__name__)

hostname_change_handler = HostnameChangeHandler()
observer = Observer()
observer.schedule(hostname_change_handler, hostname_change_handler.monitored_directory, recursive=False)
observer.start()

app.logger.info(f'Permitted domains: {" ".join(hostname_change_handler.scan_hostnames())}')


def check_domain(domain: str) -> bool:
    sampled = '.'.join(domain.split('.')[-2:])
    return sampled in hostname_change_handler.valid_hostnames


@app.route('/validate', methods=['GET'])
def main():
    domain = request.args.get('domain')
    if check_domain(domain):
        return jsonify({'message': f'Domain {domain} is valid'}), 200
    else:
        return jsonify({'message': f'Domain {domain} is not valid'}), 403
