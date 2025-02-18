from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class IPVisitorTracking(models.Model):
    _name = 'ip.visitor.tracking'
    _description = 'IP Visitor Tracking'
    _rec_name = 'ip_address'

    api_key = fields.Char(string='API Key', required=True, help='API Key from ipgeolocation.io')
    ip_address = fields.Char(string='IP Address', readonly=True)
    country = fields.Char(string='Country', readonly=True)
    city = fields.Char(string='City', readonly=True)
    longitude = fields.Float(string='Longitude', readonly=True)
    latitude = fields.Float(string='Latitude', readonly=True)
    isp = fields.Char(string='Internet Service Provider', readonly=True)
    organization = fields.Char(string='Organization', readonly=True)
    visit_time = fields.Datetime(string='Visit Time', default=fields.Datetime.now, readonly=True)

    def get_visitor_location(self):
        api_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                
                self.write({
                    'ip_address': data.get('ip'),
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'longitude': float(data.get('longitude', 0)),
                    'latitude': float(data.get('latitude', 0)),
                    'isp': data.get('isp'),
                    'organization': data.get('organization'),
                    'visit_time': fields.Datetime.now()
                })
            else:
                error_msg = f"Error al obtener datos de geolocalización. Código: {response.status_code}"
                _logger.error(error_msg)
                return {'error': error_msg}
                
        except Exception as e:
            error_msg = f"Error en la conexión con la API: {str(e)}"
            _logger.error(error_msg)
            return {'error': error_msg}