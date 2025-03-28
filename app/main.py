import logging
import os
import re

from quart import Quart, request, jsonify


required_vars = {
    'DOMAIN_REGEX',
}
missing_vars = required_vars.difference(set(os.environ))
if len(missing_vars) > 0:
    raise EnvironmentError(f"Missing vars: {' '.join(missing_vars)}")

regex = str(os.environ.get('DOMAIN_REGEX'))

VALID_DOMAIN_HTTP_RESPONSE = 200
INVALID_DOMAIN_HTTP_RESPONSE = 403


app = Quart(__name__)


try:
    compiled_regex = re.compile(regex)
except re.error as e:
    app.logger.info(f"Invalid regex: {regex})")
    raise e


logging.info(f'Registered domain regex: {regex}')
app.logger.info(f"monitored domain regex: {regex}")


@app.route('/validate', methods=['GET'])
def main():
    domain = request.args.get('domain')
    if compiled_regex.search(domain):
        return jsonify({'message': f'Domain {domain} is valid'}), VALID_DOMAIN_HTTP_RESPONSE
    else:
        return jsonify({'message': f'Domain {domain} is not valid'}), INVALID_DOMAIN_HTTP_RESPONSE
