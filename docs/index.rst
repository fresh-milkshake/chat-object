Welcome to chat-object documentation!
=====================================

.. image:: https://img.shields.io/badge/doctest-90%25_coverage-00796b
   :target: https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056
   :alt: doctest coverage

.. image:: https://img.shields.io/badge/license-MIT-blue
   :target: LICENSE.txt
   :alt: license

.. image:: https://img.shields.io/badge/python-3.10%2B-306998
   :alt: python

.. image:: https://img.shields.io/pypi/v/chat-object?color=white&label=version
   :target: https://pypi.org/project/chat-object/
   :alt: version

.. image:: https://static.pepy.tech/personalized-badge/chat-object?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=PyPI%20Downloads
   :target: https://pepy.tech/project/chat-object
   :alt: PyPI Downloads

A simple library for creating and managing chat objects and messages for LLM applications.

Features
--------

* **Simple Chat Management**: Create and manage chat conversations with ease
* **Message Objects**: Structured message handling with roles (System, User, Assistant)
* **Prompt Formatting**: Automatic indentation and formatting with the Prompt class
* **QOL Features**: Convenience functions for quick development
* **Type Safety**: Full type hints support
* **OpenAI Integration**: Seamless integration with OpenAI API

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install chat-object

Basic usage:

.. code-block:: python

   import openai
   from chat_object import Chat, Message, Role

   client = openai.OpenAI()

   chat = Chat(
       Message(Role.System, "You are a helpful assistant"),
       Message(Role.User, "Hello!")
   )

   response = client.chat.completions.create(
       model="gpt-5-nano",
       messages=chat.as_dict()
   )

   print(response.choices[0].message.content)

Installation
-------------

From PyPI:

.. code-block:: bash

   pip install chat-object

From GitHub:

.. code-block:: bash

   pip install git+https://github.com/fresh-milkshake/chat-object.git

From source:

.. code-block:: bash

   git clone https://github.com/fresh-milkshake/chat-object.git
   cd chat-object
   pip install -e .

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   examples
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
