from app.services.llm.router import router as llm_router


SYSTEM_PROMPT = """You are an expert software engineer. Generate clean, production-ready code.

Rules:
- Write complete, working code
- Include all necessary imports
- Follow language/framework best practices
- Add error handling
- Maximize code quality

Return ONLY the code block with the language identifier."""


def generate_code(prompt: str, language: str = "python", framework: str = "", context: str = "", provider: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    if context:
        messages.append({"role": "user", "content": f"Context from project:\n{context}"})
    messages.append({
        "role": "user",
        "content": f"Generate {language} code{f' using {framework}' if framework else ''} for:\n{prompt}",
    })
    return llm_router.generate(messages, provider=provider, temperature=0.3)
