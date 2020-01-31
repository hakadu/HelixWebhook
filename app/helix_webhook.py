#!/usr/bin/env python

import json
import socket
import requests
import configparser
import os 

from flask.app import Flask, request


requests.packages.urllib3.disable_warnings()
config = configparser.ConfigParser()
config.read('app/connection.ini')
app = Flask(__name__)


def push_event(body):
    body = '[' + body + ']'
    helix = config['HELIX CONNECTION']
    headers = {'Content-Type': 'application/json', 'Authorization': 'apiKey ' + helix['helix.apikey']}
    url = 'https://' + os.environ.get('HOSTNAME', 'clm-tlv-tsuw2v.bmc.com') + ":" + os.environ.get('PORT', '443') + '/tsws/api/v1.0/events'
    req = requests.post(url, headers=headers, data=body, verify=False)
    if req.status_code == 200:
        print('OK: Pushing event:' + body)
    else:
        req.raise_for_status()


def build_event_body(data):

    for alert in data['alerts']:
        status = "OPEN"
        msg = ''
        if alert['annotations']:
            if alert['annotations']['message']:
                msg = alert['annotations']['message']
            elif alert['annotations']['description']:
                msg = alert['annotations']['description']
        if data['status'].lower() == 'resolved':
            status = 'CLOSE'
        body = {'source_identifier': data['receiver'], 'object_id': data['receiver'], 'object_class': 'Prometheus',
                'severity': alert['labels']['severity'].upper(), 'class': 'Prometheus_Event',
                'object': alert['labels']['alert_name'], 'msg': msg, 'status': status, 'url': alert['generatorURL'],
                'owner': data['receiver'], 'labels': str(alert['labels']), 'annotations': str(alert['annotations'])}
        host_body = {'source_hostname': socket.getfqdn(request.remote_addr), 'source_address': request.remote_addr}
        body['source_attributes'] = host_body
        json_data = json.dumps(body)
        push_event(json_data)


@app.route('/alerts', methods=['GET', 'POST'])
def get_alerts():
    if request.method == 'POST':
        if config['GENERAL']['debug']:
            print(request.data)
        data = json.loads(request.data.decode('utf-8'))
        if type(data) is list:
            if data[0]['labels']['test_msg'] == 'Webhook setting validated':
                return 'OK'
        else:
            build_event_body(data)
            return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=config['GENERAL']['debug'])
