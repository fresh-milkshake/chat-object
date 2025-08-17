#!/usr/bin/env python3
import json
import time
from typing import List
from chat_object import Chat, Message, Role, DictMessageType


def demo_basic_usage():
    system_msg = Message(Role.System, "You are a helpful assistant for programming.")
    user_msg = Message(Role.User, "Hello! Can you help me with Python?")
    assistant_msg = Message(
        Role.Assistant, "Of course! I'd be happy to help you with Python."
    )

    chat = Chat(system_msg, user_msg, assistant_msg)
    assert len(chat) == 3
    assert chat[0].role == Role.System


def demo_dict_compatibility():
    dict_messages = [
        {"role": "system", "content": "You are a math expert."},
        {"role": "user", "content": "What is 2 + 2?"},
        {"role": "assistant", "content": "2 + 2 = 4"},
    ]
    chat = Chat(*dict_messages)

    assert chat[0]["role"] == "system"


def demo_mixed_usage():
    chat = Chat(
        {"role": "system", "content": "You are a cooking assistant."},
        Message(Role.User, "How do I make borscht?"),
        {
            "role": "assistant",
            "content": "For borscht you need: beets, cabbage, potatoes, meat...",
        },
    )

    assert len(chat) == 3
    assert isinstance(chat[0], Message)
    assert isinstance(chat[1], Message)


def demo_list_operations():
    chat = Chat()
    chat.append(Message(Role.System, "You are a travel assistant."))
    chat.append({"role": "user", "content": "Where should I go in the summer?"})

    assert len(chat) == 2

    chat.insert(0, Message(Role.System, "You are a very friendly travel assistant."))
    assert chat[0].content == "You are a very friendly travel assistant."

    chat.pop()
    assert len(chat) == 2

    chat.sort(key=lambda msg: msg.role)
    chat.clear()
    assert len(chat) == 0


def demo_json_serialization():
    chat = Chat(
        Message(Role.System, "You are a programming assistant."),
        Message(Role.User, "How do I create a function in Python?"),
        Message(
            Role.Assistant, "In Python, functions are created using the 'def' keyword."
        ),
    )

    chat_dict = chat.as_dict()
    json_str = json.dumps(chat_dict)
    loaded_dict = json.loads(json_str)
    new_chat = Chat(*loaded_dict)

    assert len(new_chat) == len(chat)


def demo_practical_scenarios():
    bot_chat = Chat(Message(Role.System, "You are a friendly chatbot. Be brief."))

    conversations = [
        ("Hello!", "Hello! How are you?"),
        ("Good, thanks!", "Glad to hear it! How can I help?"),
    ]

    for user_msg, bot_response in conversations:
        bot_chat.append(Message(Role.User, user_msg))
        bot_chat.append(Message(Role.Assistant, bot_response))
        time.sleep(0.1)

    def mock_api_call(messages: List[DictMessageType]) -> str:
        return " | ".join([f"{msg['role']}: {msg['content']}" for msg in messages])

    api_result = mock_api_call(bot_chat.as_dict())  # type: ignore
    assert "user:" in api_result
    assert "assistant:" in api_result

    user_messages = [msg for msg in bot_chat if msg.role == Role.User]
    assert len(user_messages) == 2

    assert "Hello" in bot_chat


def demo_advanced_features():
    advanced_chat = Chat(
        Message(Role.System, "You are a multifunctional assistant."),
        Message(Role.User, "Perform a math calculation: 15 * 23"),
        Message(Role.Assistant, "15 * 23 = 345"),
        Message(Role.Tool, "calculator_result: 345"),
        Message(Role.Function, "function_call: calculate(15, 23, '*')"),
    )

    role_groups = {}
    for msg in advanced_chat:
        role = msg.role
        if role not in role_groups:
            role_groups[role] = []
        role_groups[role].append(msg.content)

    assert len(role_groups) >= 4

    chat_copy = Chat(*[msg.copy() for msg in advanced_chat])
    chat_copy[0].content = "You are a modified assistant."

    assert advanced_chat[0].content != chat_copy[0].content
    assert advanced_chat != chat_copy


def main():
    demo_basic_usage()
    demo_dict_compatibility()
    demo_mixed_usage()
    demo_list_operations()
    demo_json_serialization()
    demo_practical_scenarios()
    demo_advanced_features()


if __name__ == "__main__":
    main()
