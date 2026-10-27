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

message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=messages,
)

for block in message.content:
    if block.type == "text":
        print(block.text)

# Turn 2: add Claude's reply to the history, then ask a follow-up that only
# makes sense if Claude remembers its first answer.
messages.append({"role": "assistant", "content": message.content})
messages.append(
    {
        "role": "user",
        "content": "Of those searches, which one would you start with, and why? Answer in two sentences.",
    }
)

follow_up = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=messages,
)

print("\n--- Follow-up ---\n")
for block in follow_up.content:
    if block.type == "text":
        print(block.text)
