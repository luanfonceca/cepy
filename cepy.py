#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, render_template, jsonify
from BeautifulSoup import BeautifulSoup

import requests
import re

app = Flask(__name__)

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

    response = jsonify(context)
    response.status_code = context['status']
    return response

if __name__ == "__main__":
    app.run(debug=True)
