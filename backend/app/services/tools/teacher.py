from app.services.llm.router import router as llm_router


SYSTEM_PROMPT = """You are a friendly programming teacher for beginners.

Teaching principles:
- Explain like the student is new to programming
- Use analogies and real-world examples
- Break down complex topics into small steps
- Provide code examples for every concept
- Be encouraging and patient
- Ask check-in questions to confirm understanding

Adapt your explanation level based on the student's questions."""


def teach_concept(topic: str, level: str = "beginner", context: str = "", provider: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    if context:
        messages.append({"role": "user", "content": f"Student context:\n{context}"})
    messages.append({
        "role": "user",
        "content": f"Teach me about '{topic}' at a {level} level. Include code examples and practical analogies.",
    })
    return llm_router.generate(messages, provider=provider, temperature=0.6)


def explain_error(error_message: str, code_context: str = "", provider: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\nFocus specifically on explaining errors in a beginner-friendly way."},
        {
            "role": "user",
            "content": f"Explain this error in simple terms:\n\nError: {error_message}\n\n{code_context if code_context else ''}\n\nWhat caused it and how do I fix it?",
        },
    ]
    return llm_router.generate(messages, provider=provider, temperature=0.4)
