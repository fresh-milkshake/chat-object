Examples
========

This page contains practical examples of how to use the chat-object library.

Basic Chat Usage
----------------

Create a chat object and add messages to it:

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

Using the Prompt Class
----------------------

The ``Prompt`` class automatically handles indentation and formatting:

.. code-block:: python

   from chat_object import Prompt

   # Clean indentation automatically
   prompt = Prompt("""
       You are a helpful assistant.
       Please help me with the following task:
       
       def example_function():
           return "hello world"
       
       Explain what this function does.
   """)

   # Multiple arguments are joined with newlines
   prompt = Prompt(
       "You are a helpful assistant.",
       "Please be concise in your responses.",
       "Focus on practical solutions."
   )

   # String operations work naturally
   prompt += "\n\nAdditional context here"

QOL Features for Quick Development
----------------------------------

Use convenience functions for faster development:

.. code-block:: python

   from chat_object import chat, msg_user, msg_system, msg_assistant, prmt

   # Quick chat creation
   chat_obj = chat(
       msg_system("You are a helpful assistant."),
       msg_user("Hello!"),
       msg_assistant("Hi there! How can I help you today?")
   )

   # Quick prompt creation
   prompt = prmt("You are a helpful assistant.", "Please be concise.")

Advanced Usage
--------------

Working with chat history:

.. code-block:: python

   from chat_object import Chat, Message, Role

   # Create a chat with history
   chat = Chat(
       Message(Role.System, "You are a coding assistant."),
       Message(Role.User, "Write a Python function to calculate factorial"),
       Message(Role.Assistant, "Here's a factorial function:\n\n```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n```"),
       Message(Role.User, "Can you make it iterative instead?")
   )

   # Add new messages
   chat.add_message(Message(Role.User, "What about using a loop?"))

   # Convert to OpenAI format
   messages = chat.as_dict()

   # Get just the content
   contents = chat.as_content_list()

Error Handling
--------------

Handling invalid inputs:

.. code-block:: python

   from chat_object import Message, Role

   try:
       # This will raise an error
       message = Message("invalid_role", "content")
   except ValueError as e:
       print(f"Error: {e}")

   # Valid usage
   message = Message(Role.User, "Hello")
   print(message.role)  # Role.USER
   print(message.content)  # "Hello"
