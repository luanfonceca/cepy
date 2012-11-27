-----------------------
 Cepy API
-----------------------

Como Usar
    Para trazer o endereço, em formato Json, referente ao CEP enviado, utilize a URL: ::

        http://cepy.herokuapp.com/address/<CEP>

    Modelo de Resposta: ::
        
        {
          "status": 200,
          "cep": 99999999,
          "bairro": "Lorem ipsum dolor sit amet",
          "cidade": "Ut consectetur fringilla tincidunt",
          "uf": "LI",
          "logradouro": "Nulla pellentesque euismod lobortis"
        }

HTTP Erros
    Caso o CEP não exista no banco dos Correios, ou seja passado um CEP inválido: ::

        {
          "status": 404, 
          "message": "N\u00e3o houveram resultados para este CEP."
        }