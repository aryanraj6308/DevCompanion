from app.services.llm.router import router as llm_router


SYSTEM_PROMPT = """You are an expert debugger. Analyze errors and suggest fixes.

For each issue:
1. Identify the root cause
2. Explain why it happens
3. Provide the fix with code
4. Suggest preventive measures

Be precise and actionable."""


def debug_code(code: str, error: str = "", language: str = "", context: str = "", provider: str = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    if context:
        messages.append({"role": "user", "content": f"Project context:\n{context}"})
    user_content = f"Debug this {language} code:\n\n```{language}\n{code}\n```"
    if error:
        user_content += f"\n\nError message:\n{error}"
    user_content += "\n\nIdentify all bugs and provide fixed code."
    messages.append({"role": "user", "content": user_content})
    return llm_router.generate(messages, provider=provider, temperature=0.3)
