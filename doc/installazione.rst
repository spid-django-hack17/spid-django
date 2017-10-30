Installazione
=============

Il plugin è installabile a livello utente oppure a livello sistema qualora si possiedano
privilegi di amministratore. Il consiglio è comunque quello di usare un *ambiente virtuale*
a livello utente, come ad esempio *virtualenv* (o *pyvenv* per Python 3) per non andare in
conflitto con le dipendenze di altre applicazioni Python.

Per l'installazione scegliere una directory di destinazione e poi clonare il repository:

.. code-block:: bash

  git clone https://github.com/italia/spid-django.git

eseguire poi il comando di installazione all'interno della directory di base del repo:

.. code-block:: bash

  cd spid-django/
  python pip install -r requirements.txt


Requisiti
---------

Il plugin è basato sulla libreria `python3-saml <https://github.com/onelogin/python3-saml>`_ di OneLogin.
Questa libreria ha una serie di dipendenze, da installare prima dell'installazione del plugin per SPID.

Su Linux Debian il comando per installare le dipendenze è:

.. code-block:: bash

  apt-get install libxml2-dev libxmlsec1-dev libxmlsec1-openssl

su una CentOS Linux i prerequisiti vengono invece installati con il comando:

.. code-block:: bash

  yum install libxml2-devel xmlsec1-devel xmlsec1-openssl-devel libtool-ltdl-devel

Per ulteriori dettagli consultare la documentazione della libreria
`python-xmlsec <https://github.com/mehcode/python-xmlsec>`_.

Test dell'installazione e demo
------------------------------

Per verificare se la app installata funziona si possono eseguire i test con:

.. code-block:: bash

  python manage.py test

Per eseguire la demo con il server di development di Django:

.. code-block:: bash

  python manage.py runserver

Accedere poi con un browser all'indirizzo `https://127.0.0.1:8000 <https://127.0.0.1:8000>`_
per verificare il funzionamento della demo.

Per accedere all'`admin della demo <https://127.0.0.1:8000/admin/>`_ usare *demospid* sia per il nome
utente che per la password.