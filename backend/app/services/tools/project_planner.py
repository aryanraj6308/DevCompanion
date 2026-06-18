from app.services.llm.router import router as llm_router


SYSTEM_PROMPT = """You are a senior software architect. Design project architectures.

For each project provide:
1. Overview
2. Tech stack recommendations
3. Folder structure (tree format)
4. Database schema
5. API design (endpoints)
6. Component tree (frontend)
7. Key implementation details
8. Deployment suggestions

Be practical and detailed. Optimize for maintainability."""


def create_plan(project_name: str, description: str, tech_stack: list = None, provider: str = None) -> str:
    stack_info = f"\nPreferred tech stack: {', '.join(tech_stack)}" if tech_stack else ""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Design a complete architecture for:\n\nProject: {project_name}\nDescription: {description}{stack_info}\n\nProvide a comprehensive plan.",
        },
    ]
    return llm_router.generate(messages, provider=provider, temperature=0.5)


def generate_folder_structure(project_name: str, tech_stack: list = None, provider: str = None) -> str:
    stack_info = f"\nTech stack: {', '.join(tech_stack)}" if tech_stack else ""
    messages = [
        {"role": "system", "content": "Generate a clean folder structure for a project. Use tree format."},
        {
            "role": "user",
            "content": f"Generate folder structure for: {project_name}{stack_info}",
        },
    ]
    return llm_router.generate(messages, provider=provider, temperature=0.3)
