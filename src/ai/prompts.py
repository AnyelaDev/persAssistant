"""
Prompt Templates for AI-Powered ToDo Grooming

Contains structured prompts for different AI services and grooming scenarios.
"""

PROMPT_VERSION = "1.0"

GROOMING_PROMPT_TEMPLATE = """You are an AI assistant specialized in organizing and optimizing todo lists. Your task is to improve the given todo list by:

1. Clarifying vague or unclear tasks
2. Breaking down large tasks into smaller, actionable items
3. Removing duplicates and consolidating similar items
4. Improving task descriptions for clarity
5. Suggesting logical priority ordering

Input Todo List:
{todo_list}

Please respond with a JSON object containing:
{{
    "groomed_tasks": [
        {{
            "title": "Clear, actionable task description",
            "estimated_time": "HH:MM format (optional)",
            "priority": "high|medium|low",
            "notes": "Any clarification or context",
            "source": "Reference to original input that relates to this task"
        }}
    ],
    "suggestions": ["Any general recommendations"],
    "removed_items": ["Duplicate or unnecessary items removed"],
    "processing_notes": "Brief summary of changes made"
}}

Ensure all tasks are:
- Specific and actionable
- Clearly worded
- Appropriately sized (can be completed in reasonable time)
- Free of duplicates
- Alert of any logic inconsistency

Respond ONLY with valid JSON, no additional text."""

SIMPLE_GROOMING_PROMPT = """Improve this todo list by making tasks clearer and removing duplicates:

{todo_list}

Respond with JSON:
{{
    "groomed_tasks": [
        {{"title": "task description", "priority": "medium"}}
    ],
    "processing_notes": "what was changed"
}}"""

LONG_LIST_PROMPT_TEMPLATE = """You are organizing a large todo list. Focus on:
- Grouping related tasks
- Identifying urgent vs non-urgent items
- Breaking down complex tasks
- Removing duplicates

{base_template}

Special instructions for large lists:
- Group related tasks into categories
- Identify and separate urgent vs non-urgent items
- Suggest task batching opportunities"""


def get_grooming_prompt(todo_list: str, prompt_type: str = "standard") -> str:
    """
    Get formatted prompt for todo list grooming.
    
    Args:
        todo_list: The user's raw todo list text
        prompt_type: Type of prompt ("standard", "simple", "long")
        
    Returns:
        Formatted prompt string
    """
    todo_list = todo_list.strip()
    
    if prompt_type == "simple":
        return SIMPLE_GROOMING_PROMPT.format(todo_list=todo_list)
    elif prompt_type == "long":
        base_template = GROOMING_PROMPT_TEMPLATE
        return LONG_LIST_PROMPT_TEMPLATE.format(
            base_template=base_template,
            todo_list=todo_list
        )
    else:  # standard
        return GROOMING_PROMPT_TEMPLATE.format(todo_list=todo_list)


def select_prompt_type(todo_list: str) -> str:
    """
    Automatically select appropriate prompt type based on todo list characteristics.
    
    Args:
        todo_list: The user's raw todo list text
        
    Returns:
        Prompt type identifier
    """
    lines = [line.strip() for line in todo_list.split('\n') if line.strip()]
    
    if len(lines) > 10:
        return "long"
    elif len(lines) <= 3:
        return "simple"
    else:
        return "standard"