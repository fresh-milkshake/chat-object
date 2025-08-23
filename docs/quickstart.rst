Quick Start Guide
=================

This guide will help you get started with chat-object in just a few minutes.

Installation
------------

Install the package using pip:

.. code-block:: bash

   pip install chat-object

First Steps
-----------

1. **Import the library**:

   .. code-block:: python

      from chat_object import Chat, Message, Role

2. **Create your first chat**:

   .. code-block:: python

      chat = Chat(
          Message(Role.System, "You are a helpful assistant"),
          Message(Role.User, "Hello!")
      )

3. **Use with OpenAI**:

   .. code-block:: python

      import openai
      
      client = openai.OpenAI()
      response = client.chat.completions.create(
          model="gpt-5-nano",
          messages=chat.as_dict()
      )

4. **Add the response to your chat**:

   .. code-block:: python

      chat.add_message(Message(Role.Assistant, response.choices[0].message.content))

Complete Example
----------------

Here's a complete working example:

.. code-block:: python

   import openai
   from chat_object import Chat, Message, Role

   # Initialize OpenAI client
   client = openai.OpenAI()

   # Create a chat with system message
   chat = Chat(
       Message(Role.System, "You are a helpful coding assistant. Provide concise answers.")
   )

   # Add user message
   chat.add_message(Message(Role.User, "Write a Python function to reverse a string"))

   # Get response from OpenAI
   response = client.chat.completions.create(
       model="gpt-5-nano",
       messages=chat.as_dict()
   )

   # Add assistant response to chat
   assistant_message = response.choices[0].message.content
   chat.add_message(Message(Role.Assistant, assistant_message))

   # Continue the conversation
   chat.add_message(Message(Role.User, "Can you make it handle None values?"))

   # Get another response
   response = client.chat.completions.create(
       model="gpt-5-nano",
       messages=chat.as_dict()
   )

   print(response.choices[0].message.content)

Using QOL Functions
-------------------

For even faster development, use the convenience functions:

.. code-block:: python

   from chat_object import chat, msg_system, msg_user, msg_assistant

   # Quick chat creation
   chat_obj = chat(
       msg_system("You are a helpful assistant"),
       msg_user("Hello!"),
       msg_assistant("Hi there! How can I help you?")
   )

   # Add more messages easily
   chat_obj.add_message(msg_user("What's the weather like?"))

Using the Prompt Class
----------------------

For better prompt formatting:

.. code-block:: python

   from chat_object import Prompt

   # Automatic indentation cleanup
   prompt = Prompt("""
       You are a helpful assistant.
       
       Please help me with this code:
       
       def example():
           return "hello"
   """)

   print(prompt)  # Clean, properly formatted prompt

Next Steps
----------

- Read the :doc:`examples` for more advanced usage
- Check the :doc:`api` for complete API reference
- Explore the source code on `GitHub <https://github.com/fresh-milkshake/chat-object>`_
