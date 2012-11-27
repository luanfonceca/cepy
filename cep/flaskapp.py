#!/usr/bin/env python
# encoding: utf-8
import os
import re
import flask
import requests
from BeautifulSoup import BeautifulSoup


class Application(flask.Flask):
    '''I am the core flask application.'''

    def __init__(self, config_envvar='APP_CONFIG'):
        flask.Flask.__init__(self, __package__)
        self.config['HOST'] = os.environ.get('HOST', '0.0.0.0')
        self.config['PORT'] = int(os.environ.get('PORT', '5000'))
        self.config['DEBUG'] = bool(os.environ.get('DEBUG'))
        self.config['SECRET_KEY'] = os.urandom(24)
        self.config.from_envvar(config_envvar, silent=True)

    def run(self, *args, **kwds):
        kwds.setdefault('debug', self.config['DEBUG'])
        kwds.setdefault('port', self.config['PORT'])
        kwds.setdefault('host', self.config['HOST'])
        flask.Flask.run(self, *args, **kwds)


def create_application(*args, **kwds):
    app = Application(*args, **kwds)

    @app.route('/')
    def index():
        return '<pre>Usage:\n\tTo get the address: "/address/99999999"</pre>'

    @app.route('/address/<int:cep>')
    @app.route('/address/<string:cep>')
    def address(cep):
        if type(cep) is str: cep = re.sub('\D', '', cep)

        def split_city_from_uf(str):
            return str.replace('\n%s\n%s' % (' '*32, '\t'*8), '').split('/')

        url = 'http://m.correios.com.br/movel/buscaCepConfirma.do'
        data = {'metodo': 'buscarCep', 'cepEntrada': cep}
        r = requests.post(url, data)

        attrs = {'class': 'respostadestaque'}
        soup = BeautifulSoup(r.text).findAll('span', attrs)
    
        try:
            context = {
                'logradouro': soup[0].text,
                'bairro': soup[1].text,
                'cidade': split_city_from_uf(soup[2].text)[0],
                'uf': split_city_from_uf(soup[2].text)[1],
                'cep': cep,
                'status': 200,
            }
        except IndexError:
            context = {
                'message': u'Não houveram resultados para este CEP.',
                'status': 404,
            }
        
        response = flask.jsonify(context)
        response.status_code = context['status']
        return response

    return app

