# Gemini Chat

This document provides an overview of the Gemini Chat functionality, based on the provided code snippets.

## Introduction

The Gemini Chat system is designed to provide a flexible and powerful way to interact with Gemini language models. It supports both single-turn and multi-turn conversations, streaming and non-streaming responses, and can be integrated with a variety of frontend applications.

## Core Components

The chat system is composed of several key components:

*   **The `chat` method:** The main entry point for handling chat requests.
*   **The `Chat` data model:** Represents a chat session.
*   **The `GeminiModel` class:** A wrapper for the Gemini model API.
*   **Frontend components:** For rendering chat messages in a user interface.
*   **Message formatting and templates:** To ensure messages are sent to the model in the correct format.

### The `chat` method

The `chat` method is the heart of the chat system. It is responsible for:

*   Receiving a `ChatRequest` object.
*   Building a list of messages for the language model.
*   Preparing the parameters for the API call.
*   Calling the Gemini language model API.
*   Returning the model's response, either as a single object or a stream.

```python
def chat(
        self,
        request: ChatRequest,
        strategy_chain: Optional[List[Type[SystemPromptStrategy]]] = None,
        stream: bool = True,
        json_response: bool = False,
        client: Optional[Any] = None,
        model_params: Optional[Dict[str, Any]] = None,
        context: Optional[Any] = None,
    ) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
    """
    Main chat method supporting both streaming and non-streaming responses
    ... 
    """
```

### The `Chat` Data Model

The `Chat` class represents a single chat session. It contains information about the session, such as the session ID, title, summary, and creation time.

```python
class Chat:
    def __init__(
        self,
        sessionId: str = "",
        summary: str = "",
        title: str = "",
        createTime: str = "",
    ) -> None:
        self.session_id = sessionId
        self.summary = summary
        self.title = title
        self.create_time = createTime
```

### The `GeminiModel` Class

The `GeminiModel` class provides a convenient way to interact with the Gemini API. It handles the details of making API calls, including retries and parallel requests.

```python
class GeminiModel:
    """Class for the Gemini model."""

    def __init__(
        self,
        model_name: str = "gemini-2.0-flash-001",
        ...
    ):
        ...

    def call(self, prompt: str, parser_func=None) -> str:
        """Calls the Gemini model with the given prompt."""
        ...

    def call_parallel(
        self,
        prompts: List[str],
        ...
    ) -> List[Optional[str]]:
        """Calls the Gemini model for multiple prompts in parallel..."""
        ...
```

### Frontend Components

The chat system is designed to be used with a variety of frontend applications. The provided snippets show examples of how to render chat messages in a React application.

The `ChatMessage` interface defines the structure of a chat message object:

```typescript
interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: string;
}
```

This can be used in a React component like this:

```jsx
(message, index) => (
  <ChatMessage
    key={message.id}
    isLoading={
      streaming &&
      !streamContent &&
      index === messages.length - 1 &&
      message.role === 'assistant'
    }
    message={message.content}
    role={message.role}
    timestamp={message.timestamp}
  />
)
```

### Message Formatting

The `apply_chat_template` method is used to format a list of messages into a single string that can be sent to the language model. This is important for models that require a specific input format.

```python
def apply_chat_template(self, messages: list):
    text_with_audio = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        ...
        text_with_audio += f"<|BOT|>{role}\n{content}<|EOT|>".
    ...
    return text_with_audio
```

### Group Chat

The system also includes functionality for group chats. The `_publish_group_chat_message` method can be used to publish messages to a group chat topic.

```python
async def _publish_group_chat_message(
        self,
        content: str,
        ...
    ) -> None:
    """Helper function to publish a group chat message."""
    ...
```

### Configuration and Testing

The `setup_gemini_config` function shows how to create a custom evaluation configuration for the Gemini model. The `mock_gemini_session` and `gemini_llm` functions are provided for testing purposes.

```python
def setup_gemini_config():
    """
    Create a custom evaluation configuration using Gemini 2.0 Flash via OpenRouter
    """
    ...

def mock_gemini_session():
  """Mock Gemini session for testing."""
  return mock.AsyncMock()

def gemini_llm():
  return Gemini(model="gemini-1.5-flash")
```
