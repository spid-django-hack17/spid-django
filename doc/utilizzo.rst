Utilizzo
========

Per utilizzare il login con SPID aggiungere 'spid' alla lista INSTALLED_APPS
nel file `setting.py` del progetto:

.. code-block:: python

    INSTALLED_APPS = [
        ... ,
        'spid'
    ]

Sempre in `setting.py` aggiungere le configurazioni del service provider SPID come nel seguente
esempio:

.. code-block:: python

    #
    # SPID Configuration
    SPID_SP_DOMAIN = "localhost:8000/spid"
    SPID_SERVICE_NAME = "apptest"
    SPID_SERVICE_DESCRIPTION = "Demo SP test app"
    SPID_REQUESTED_ATTRIBUTES = ['name', 'familyName', 'fiscalNumber', 'spidCode']
    SPID_SP_PUBLIC_CERT = os.path.join(BASE_DIR, 'demo/certs/demo.crt')
    SPID_SP_PRIVATE_KEY = os.path.join(BASE_DIR, 'demo/certs/demo.key')

I parametri di configurazione sono necessari per comporre il file XML dei metadati del
Service Provider e hanno il seguente significato:

.. py:attribute:: SPID_SP_DOMAIN

    Dominio operativo del Service Provider per comporre la URL di accesso `entityID`.

.. py:attribute:: SPID_SERVICE_NAME

    Nome del servizio.

.. py:attribute:: SPID_SERVICE_DESCRIPTION

    Descrizione del servizio.

.. py:attribute:: SPID_REQUESTED_ATTRIBUTES

    Attributi SPID necessari al servizio.

.. py:attribute:: SPID_SP_PUBLIC_CERT

    Path al certificato pubblico x509 inserito nei metadati che serve a decodificare
    le richieste SAML del Service Provider.

.. py:attribute:: SPID_SP_PRIVATE_KEY

    Path alla chiave SSL usata per la criptazione delle richieste SAML del Service Provider.


Una volta configurato il progetto si può abilitare il login SAML nelle viste inserendo il CSS e lo
script jQuery del bottone. Per l'inserimento nel template bisogna inserire i seguenti tag in modo
che appaiano nella sezione *<head>* delle pagine HTML da usare per l'accesso SPID:

.. code-block:: html

    <link type="text/css" rel="stylesheet" href="/static/spid/css/spid-sp-access-button.min.css" />
    <script type="text/javascript" src="/static/spid/js/jquery.min.js"></script>
    <script type="text/javascript" src="/static/spid/js/spid-sp-access-button.min.js"></script>

In alternativa si possono inserire le medesime risorse specificandole nelle meta informazioni delle classi
delle viste, per questo fare riferimento alla `documentazione di Django <https://docs.djangoproject.com>`_.

Nel singolo template includere all'inizio il tag load per caricare i tag di SPID:

.. code-block:: django

   {% extends "base.html" %}
   {% load spid_tags %}
   ...

e poi inserire nel template il bottone usando l'apposito template tag *spid_button*:

.. code-block:: django

    {% spid_button 'large' %}



