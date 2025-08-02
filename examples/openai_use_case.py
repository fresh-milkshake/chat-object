import os
import sys
from typing import Optional
from dotenv import load_dotenv

load_dotenv(override=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chat_object import (  # noqa: E402
    msgs,
    chat,
    prmt,
    msg_user,
    msg_assistant,
    msg_system,
    Role,
)

try:
    import openai
except ImportError:
    print("❌ OpenAI package not installed. Install it with: pip install openai")
    print("This example requires the OpenAI package to work.")
    sys.exit(1)


class CodeReviewAssistant:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print(
                "❌ OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )
            print("You can get an API key from: https://platform.openai.com/api-keys")
            sys.exit(1)

        openai.api_key = self.api_key

        self.system_prompt = prmt("""
            You are an expert code reviewer and Python developer.
            
            Your role is to:
            1. Review code for best practices, bugs, and improvements
            2. Suggest optimizations and better patterns
            3. Explain your reasoning clearly
            4. Provide specific, actionable feedback
            
            Always be constructive and educational in your feedback.
            Focus on both correctness and code quality.
        """)

        self.chat = chat()
        self._initialize_chat()

    def _initialize_chat(self):
        self.chat.add(msg_system(self.system_prompt))

    def review_code(
        self, code: str, language: str = "Python", context: str = ""
    ) -> str:
        """
        Review a piece of code and provide feedback.

        Args:
            code: The code to review
            language: Programming language of the code
            context: Additional context about the code

        Returns:
            AI response with code review feedback
        """
        user_prompt = prmt(f"""
            Please review this {language} code:
            
            {code}
            
            {f"Context: {context}" if context else ""}
            
            Provide a comprehensive code review including:
            1. Potential bugs or issues
            2. Code quality improvements
            3. Performance optimizations
            4. Best practices suggestions
            5. Security considerations (if applicable)
        """)

        self.chat.add(msg_user(user_prompt))

        try:
            response = self._get_ai_response()
            self.chat.add(msg_assistant(response))
            return response

        except Exception as e:
            error_msg = f"Error getting AI response: {e}"
            print(f"❌ {error_msg}")
            return error_msg

    def suggest_improvements(self, code: str, specific_issue: str = "") -> str:
        """
        Suggest specific improvements for code.

        Args:
            code: The code to improve
            specific_issue: Specific issue to focus on

        Returns:
            AI response with improvement suggestions
        """
        improvement_prompt = prmt(f"""
            Here's some code that needs improvement:
            
            {code}
            
            {f"Focus on this specific issue: {specific_issue}" if specific_issue else "Suggest general improvements"}
            
            Please provide:
            1. Specific code improvements with examples
            2. Alternative approaches
            3. Explanation of why these changes are better
            4. Any potential trade-offs to consider
        """)

        self.chat.add(msg_user(improvement_prompt))

        try:
            response = self._get_ai_response()
            self.chat.add(msg_assistant(response))
            return response
        except Exception as e:
            return f"Error: {e}"

    def explain_code(self, code: str) -> str:
        """
        Explain what a piece of code does.

        Args:
            code: The code to explain

        Returns:
            AI response explaining the code
        """
        explain_prompt = prmt(f"""
            Please explain what this code does:
            
            {code}
            
            Provide:
            1. A clear, high-level explanation
            2. Step-by-step breakdown of the logic
            3. Key concepts and patterns used
            4. Potential use cases
        """)

        self.chat.add(msg_user(explain_prompt))

        try:
            response = self._get_ai_response()
            self.chat.add(msg_assistant(response))
            return response
        except Exception as e:
            return f"Error: {e}"

    def _get_ai_response(self) -> str:
        try:
            messages = []
            for m in self.chat:
                messages.append({"role": m.role, "content": m.content})

            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )

            content = response.choices[0].message.content
            if content is None:
                return "No response content received"
            return content

        except openai.OpenAIError as e:
            raise Exception(f"OpenAI API error: {e}")

    def get_chat_history(self) -> str:
        return str(self.chat)

    def clear_history(self):
        self.chat.clear()
        self._initialize_chat()


def main():
    print("🤖 CODE REVIEW ASSISTANT DEMO")
    print("=" * 50)
    print("This example uses chat-object components with OpenAI API")
    print("to create a practical code review assistant.\n")

    assistant = CodeReviewAssistant()

    print("📝 EXAMPLE 1: Code Review")
    print("-" * 30)

    sample_code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Test the function
result = calculate_fibonacci(10)
print(f"Fibonacci(10) = {result}")
"""

    print("Code to review:")
    print(sample_code)

    print("\n🤖 AI Review:")
    review = assistant.review_code(
        sample_code, "Python", "This is a recursive Fibonacci implementation"
    )
    print(review)

    print("\n\n🔧 EXAMPLE 2: Code Improvements")
    print("-" * 30)

    inefficient_code = """
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates
"""

    print("Code to improve:")
    print(inefficient_code)

    print("\n🤖 AI Suggestions:")
    improvements = assistant.suggest_improvements(
        inefficient_code, "performance optimization"
    )
    print(improvements)

    print("\n\n📚 EXAMPLE 3: Code Explanation")
    print("-" * 30)

    complex_code = """
from functools import reduce
from typing import List, Callable

def compose(*functions: Callable) -> Callable:
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x ** 2

# Usage
pipeline = compose(square, multiply_by_two, add_one)
result = pipeline(5)  # ((5^2) * 2) + 1 = 51
"""

    print("Code to explain:")
    print(complex_code)

    print("\n🤖 AI Explanation:")
    explanation = assistant.explain_code(complex_code)
    print(explanation)

    print("\n\n💬 EXAMPLE 4: Chat History")
    print("-" * 30)
    print("Full conversation history:")
    print(assistant.get_chat_history())

    print("\n\n🎯 EXAMPLE 5: Advanced Prompt Usage")
    print("-" * 30)

    template = prmt("""
        You are a {{role}} expert.
        
        Task: {{task}}
        
        Code:
        {{code}}
        
        Please provide {{type}} feedback.
    """)

    filled_prompt = template.replace("{{role}}", "Python security")
    filled_prompt = filled_prompt.replace("{{task}}", "security audit")
    filled_prompt = filled_prompt.replace(
        "{{code}}", "import os; os.system('rm -rf /')"
    )
    filled_prompt = filled_prompt.replace("{{type}}", "security-focused")

    print("Template prompt:")
    print(template)
    print("\nFilled prompt:")
    print(filled_prompt)

    print("\n\n🔗 EXAMPLE 6: Component Integration")
    print("-" * 30)

    messages = msgs(
        (Role.System, "You are a helpful coding assistant."),
        (Role.User, "How do I write a decorator in Python?"),
        (Role.Assistant, "Here's how to write a decorator..."),
        (Role.User, "Can you show me an example?"),
        (Role.Assistant, "Sure! Here's an example..."),
    )

    demo_chat = chat(*messages)

    print(f"Chat has {len(demo_chat)} messages")
    print("Message roles:", [m.role for m in demo_chat])

    print(f"Contains 'decorator': {'decorator' in demo_chat}")

    chat_dict = demo_chat.as_dict()
    print(f"Chat as dictionary: {len(chat_dict)} messages")

    print("\n✅ Demo completed!")
    print("\nThis example demonstrates:")
    print("• Using Prompt class for structured prompts")
    print("• Using Message class for chat messages")
    print("• Using Chat class for conversation management")
    print("• Integration with real AI APIs")
    print("• Practical code review functionality")


if __name__ == "__main__":
    main()
