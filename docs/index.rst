.. raw:: html

   <p align="center">
   <a href="https://github.com/fresh-milkshake/chat-object">
      <img src="_static/logo.svg" alt="chat-object logo" width="180" />
   </a>
   <br />
   <br />
   <b><span style="font-size:2.2em;">chat-object</span></b>
   <br />
   <em>Elegant, Pythonic chat/message objects for LLMs</em>
   </p>


Overview
===========

.. image:: https://img.shields.io/badge/doctest-90%25_coverage-00796b
   :target: https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056
   :alt: doctest coverage

.. image:: https://img.shields.io/badge/license-MIT-blue
   :target: LICENSE.txt
   :alt: license

.. image:: https://img.shields.io/badge/python-3.10%2B-306998
   :alt: python version

.. image:: https://img.shields.io/pypi/v/chat-object?color=white&label=version
   :target: https://pypi.org/project/chat-object/
   :alt: PyPI version

.. image:: https://static.pepy.tech/personalized-badge/chat-object?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=PyPI%20Downloads
   :target: https://pepy.tech/project/chat-object
   :alt: PyPI Downloads


``chat-object`` is a lightweight, intuitive Python library for building, managing, and formatting chat messages for LLM (Large Language Model) applications. Effortlessly create chat histories, prompts, and message objects that work seamlessly with OpenAI, Anthropic, and other LLM APIs.

Features
--------

- **Simple, Pythonic API** for chat and prompt construction
- **Automatic formatting** for OpenAI/Anthropic message schemas
- **Convenience utilities** for rapid prototyping and development
- **Type-safe, explicit roles** (``System``, ``User``, ``Assistant``)
- **Flexible prompt composition** with natural string operations

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
