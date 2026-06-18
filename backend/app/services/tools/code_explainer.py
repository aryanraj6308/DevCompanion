from app.services.llm.router import router as llm_router


SYSTEM_PROMPT = """You are an expert programming teacher. Explain code clearly and concisely.

Focus on:
- What the code does
- How it works step by step
- Key concepts and patterns used
- Potential improvements

Use simple language. Include examples when helpful."""


def explain_code(code: str, language: str = "", context: str = "", provider: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    if context:
        messages.append({"role": "user", "content": f"Additional context:\n{context}"})
    messages.append({
        "role": "user",
        "content": f"Explain this {language} code:\n\n```{language}\n{code}\n```",
    })
    return llm_router.generate(messages, provider=provider, temperature=0.4)
