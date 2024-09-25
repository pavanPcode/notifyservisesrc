from flask import jsonify
import requests


class RequestAPI:
    def callapi(self,serviceurl):
        try:
            response = requests.get(serviceurl)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                return jsonify(data)
            else:
                
                return jsonify({'error': 'Failed to fetch data from the other service'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500