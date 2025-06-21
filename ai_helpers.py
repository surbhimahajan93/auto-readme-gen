"""
AI Helpers Module

This module provides AI-powered enhancements for README generation.
It can optionally use AI services to improve README content.
"""

import os
from pathlib import Path
from typing import Optional


def enhance_readme_with_ai(readme_content: str, project_path: Path) -> str:
    """
    Enhance README content using AI services.
    
    This is a placeholder function that can be extended to use
    various AI services like OpenAI, Claude, or local models.
    
    Args:
        readme_content: The current README content
        project_path: Path to the project directory
    
    Returns:
        str: Enhanced README content
    """
    # For now, return the original content
    # This can be extended to use AI services like:
    # - OpenAI GPT models
    # - Anthropic Claude
    # - Local models via Ollama
    # - GitHub Copilot API
    
    # Example implementation structure:
    # try:
    #     # Analyze project structure
    #     project_info = analyze_project_structure(project_path)
    #     
    #     # Call AI service
    #     enhanced_content = call_ai_service(readme_content, project_info)
    #     
    #     return enhanced_content
    # except Exception as e:
    #     print(f"AI enhancement failed: {e}")
    #     return readme_content
    
    return readme_content


def analyze_project_structure(project_path: Path) -> dict:
    """
    Analyze project structure for AI enhancement.
    
    Args:
        project_path: Path to the project directory
    
    Returns:
        dict: Project analysis information
    """
    analysis = {
        'project_name': project_path.name,
        'file_count': 0,
        'languages': set(),
        'has_tests': False,
        'has_docs': False,
        'has_config': False,
        'main_files': []
    }
    
    # Count files and detect languages
    for root, dirs, files in os.walk(project_path):
        # Skip common ignored directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules'}]
        
        for file in files:
            analysis['file_count'] += 1
            
            if file.endswith('.py'):
                analysis['languages'].add('Python')
            elif file.endswith(('.js', '.ts')):
                analysis['languages'].add('JavaScript/TypeScript')
            elif file.endswith('.java'):
                analysis['languages'].add('Java')
            elif file.endswith('.go'):
                analysis['languages'].add('Go')
            elif file.endswith('.rs'):
                analysis['languages'].add('Rust')
            elif file.endswith('.md'):
                analysis['has_docs'] = True
            elif file.endswith(('.json', '.yaml', '.yml', '.toml')):
                analysis['has_config'] = True
            elif 'test' in file.lower() or 'spec' in file.lower():
                analysis['has_tests'] = True
            elif file in ['main.py', 'app.py', 'index.js', 'main.go']:
                analysis['main_files'].append(file)
    
    analysis['languages'] = list(analysis['languages'])
    
    return analysis


def call_ai_service(content: str, project_info: dict) -> str:
    """
    Call an AI service to enhance README content.
    
    This is a placeholder function that can be implemented to use
    various AI services.
    
    Args:
        content: Current README content
        project_info: Project analysis information
    
    Returns:
        str: Enhanced README content
    """
    # Example implementation for OpenAI:
    # import openai
    # 
    # client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # 
    # prompt = f"""
    # Enhance this README for a {project_info['languages']} project:
    # 
    # {content}
    # 
    # Make it more engaging, add relevant details based on the project type,
    # and improve the overall structure while keeping the existing information.
    # """
    # 
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # 
    # return response.choices[0].message.content
    
    return content


def setup_ai_environment() -> bool:
    """
    Setup AI environment and check for required API keys.
    
    Returns:
        bool: True if AI services are available, False otherwise
    """
    # Check for common AI service API keys
    ai_keys = {
        'openai': 'OPENAI_API_KEY',
        'anthropic': 'ANTHROPIC_API_KEY',
        'cohere': 'COHERE_API_KEY'
    }
    
    available_services = []
    for service, key_name in ai_keys.items():
        if os.getenv(key_name):
            available_services.append(service)
    
    if available_services:
        print(f"Available AI services: {', '.join(available_services)}")
        return True
    else:
        print("No AI services configured. Using basic README generation.")
        return False
