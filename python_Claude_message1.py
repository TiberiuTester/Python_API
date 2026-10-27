import anthropic

client = anthropic.Anthropic()

# The API is stateless: Claude only sees what's in this list, so we keep the
# whole conversation here and send it with every request.
messages = [
    {
        "role": "user",
        "content": "What should I search for to find the latest developments in renewable energy?",
    }
]

# Streaming: instead of waiting for the full answer, print each piece of text
# the moment it arrives. end="" keeps it on one line, flush=True shows it now.
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    # After the stream ends, get the complete message (same object that
    # messages.create() returns) so we can save it in the history.
    message = stream.get_final_message()

# Turn 2: add Claude's reply to the history, then ask a follow-up that only
# makes sense if Claude remembers its first answer.
messages.append({"role": "assistant", "content": message.content})
messages.append(
    {
        "role": "user",
        "content": "Of those searches, which one would you start with, and why? Answer in two sentences.",
    }
)

print("\n\n--- Follow-up ---\n")
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=messages,
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

    follow_up = stream.get_final_message()

print(f"\n\nTokens used - turn 1: {message.usage.output_tokens} out, "
      f"turn 2: {follow_up.usage.input_tokens} in / {follow_up.usage.output_tokens} out")
