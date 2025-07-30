# chat-object

[![doctest coverage](https://img.shields.io/badge/doctest-90%25_coverage-green)](https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056)
[![license](https://img.shields.io/badge/license-MIT-lightblue)](LICENSE.txt)
![python](https://img.shields.io/badge/python-3.8%2B-blue)

A simple library for creating and managing chat objects and messages for LLM applications.

## Installation

```bash
pip install chat-object
```

## Quick Start

```python
import openai
from chat_object import Chat, Message, Role

client = openai.OpenAI()

chat = Chat(
    Message(Role.System, "You are a helpful assistant"),
    Message(Role.User, "Hello!")
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=chat.as_dict()
)

print(response.choices[0].message.content)
```

> [!TIP]
> See [example_usage.py](example_usage.py) for more examples.

## Features

- **Well-tested code**: Comprehensive test coverage with doctests throughout the codebase ([90% coverage](https://gist.github.com/fresh-milkshake/48a14bcc9c753a99d0af6935eb96e056))
- **Type safety**: Full type hints and enum-based roles
- **Backward compatibility**: almost seamless integration with existing APIs
- **Immutable design**: Safe message handling with copy methods

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.