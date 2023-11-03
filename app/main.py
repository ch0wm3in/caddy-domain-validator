import os

from quart import Quart, request, jsonify
from watchdog.observers import Observer

from handler import HostnameChangeHandler

required_vars = {
    'SITE_DIRECTORY',
}
missing_vars = required_vars.difference(set(os.environ))
if len(missing_vars) > 0:
    raise EnvironmentError(f"Missing vars: {' '.join(missing_vars)}")

monitored_directory = os.environ.get('SITE_DIRECTORY')
VALID_DOMAIN_HTTP_RESPONSE = 200
INVALID_DOMAIN_HTTP_RESPONSE = 403


app = Quart(__name__)

hostname_change_handler = HostnameChangeHandler(directory=monitored_directory)
hostname_change_handler.scan_directory()

observer = Observer()
observer.schedule(hostname_change_handler, monitored_directory, recursive=False)
observer.start()

app.logger.info(f'Permitted domains: {" ".join(hostname_change_handler.valid_hostnames)}')


def check_domain(domain: str) -> bool:
    # sampled = '.'.join(domain.split('.')[-2:])
    # return sampled in hostname_change_handler.valid_hostnames
    return domain in hostname_change_handler.valid_hostnames


@app.route('/validate', methods=['GET'])
def main():
    domain = request.args.get('domain')
    if check_domain(domain):
        return jsonify({'message': f'Domain {domain} is valid'}), VALID_DOMAIN_HTTP_RESPONSE
    else:
        return jsonify({'message': f'Domain {domain} is not valid'}), INVALID_DOMAIN_HTTP_RESPONSE
