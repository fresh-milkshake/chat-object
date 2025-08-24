<p align="center">
  <a href="https://github.com/fresh-milkshake/chat-object">
    <img src="assets/logo.svg" alt="chat-object logo" width="180" />
  </a>
  <br />
  <b><span style="font-size:2.2em;">chat-object</span></b>
  <br />
  <em>Elegant, Pythonic chat/message objects for LLMs</em>
</p>

#

[![doctest coverage](https://img.shields.io/badge/doctest-90%25_coverage-00796b)](https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE.txt)
![python](https://img.shields.io/badge/python-3.10%2B-306998)
[![version](https://img.shields.io/pypi/v/chat-object?color=white&label=version)](https://pypi.org/project/chat-object/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/chat-object?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=PyPI%20Downloads)](https://pepy.tech/project/chat-object)


`chat-object` is a lightweight, intuitive Python library for building, managing, and formatting chat messages for LLM (Large Language Model) applications. Effortlessly create chat histories, prompts, and message objects that work seamlessly with OpenAI, Anthropic, and other LLM APIs.


## Features

- **Simple, Pythonic API** for chat and prompt construction
- **Automatic formatting** for OpenAI/Anthropic message schemas
- **Convenience utilities** for rapid prototyping and development
- **Type-safe, explicit roles** (`System`, `User`, `Assistant`)
- **Flexible prompt composition** with natural string operations



## Installation

From PyPI:

```bash
pip install chat-object
```

From GitHub:

```bash
pip install git+https://github.com/fresh-milkshake/chat-object.git
```

Or from source:

```bash
git clone https://github.com/fresh-milkshake/chat-object.git
cd chat-object
pip install -e .
```

## Quick Start

### Basic Chat Usage

Create a chat object and add messages to it:

```python
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
```

### Using the Prompt Class

The `Prompt` class automatically handles indentation and formatting:

```python
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
```

### QOL Features for Quick Development

Use convenience functions for faster development:

```python
from chat_object import chat, msg_user, msg_system, msg_assistant, prmt

# Quick chat creation
chat_obj = chat(
    msg_system("You are a helpful assistant."),
    msg_user("Hello!"),
    msg_assistant("Hi there! How can I help you today?")
)

# Quick prompt creation
prompt = prmt("You are a helpful assistant.")

# Convert to dict for API calls
messages = chat_obj.as_dict()
```

> [!TIP]
> See [examples](examples) folder for more comprehensive examples.

## Features

- **Well-tested code**: Comprehensive test coverage with doctests throughout the codebase ([90% coverage](https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056))
- **Type safety**: Full type hints and enum-based roles
- **Backward compatibility**: seamless integration with existing APIs like OpenAI, Anthropic, Together, Ollama, etc.
- **QOL features**: Quick and easy message creation with `msg_user`, `msg_assistant`, `msg_system`, `prmt`, `msgs`, `chat` (Recommended, but not required). Pretty rich example usage of qol features is in [examples/openai_use_case.py](examples/openai_use_case.py).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
