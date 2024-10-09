import logging
import os
from pathlib import Path

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

p = Path(monitored_directory)
directories = (x for x in p.iterdir() if x.is_dir())

# All directories. So /site/A, /site/B. This would be A, B
segment_set = set()

# All domains, so /site/A/apple.com, would be apple.com
domain_set = set()

observer = Observer()
for directory in directories:
    abs_dir = directory.absolute()
    segment_set.add(directory.name)
    hostname_change_handler = HostnameChangeHandler(directory=abs_dir,
                                                    root_directory=monitored_directory,
                                                    domain_set=domain_set,
                                                    segment_set=segment_set,
                                                    )
    observer.schedule(hostname_change_handler, abs_dir, recursive=False)

observer.start()

logging.info(f'Registered segments: {segment_set}')
app.logger.info(f"monitored directory: {monitored_directory}")
app.logger.info(f'Permitted domains: {" ".join(hostname_change_handler.valid_hostnames)}')


@app.route('/validate', methods=['GET'])
def main():
    domain = request.args.get('domain')
    if domain in domain_set:
        return jsonify({'message': f'Domain {domain} is valid'}), VALID_DOMAIN_HTTP_RESPONSE
    else:
        return jsonify({'message': f'Domain {domain} is not valid'}), INVALID_DOMAIN_HTTP_RESPONSE
