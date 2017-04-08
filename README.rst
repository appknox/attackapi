attackapi
===========

attack api is a cli tool to find security vulnerabilities in an API.

It uses mitmproxy to setup proxy and syntribos to detect vulnerabilities in API. To find security vulnerabilities a mobile app or web app, use attackapi as proxy and just visit all the pages/api which needs to be checked.


Installation
================

.. code-block:: shell

    $ pip install attackapi

attackapi uses redis to store requests and for inter process communication. Make sure redis is installed and running on your system.


Usage
=========

To see help

.. code-block:: shell

    $ attackapi --help


To start a proxy and attack API

.. code-block:: shell

    $ attackapi run
