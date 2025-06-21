"""
README Generator Module

This module provides functionality to automatically generate README files
by analyzing project structure, dependencies, and code.
"""

__all__ = ["generate_readme", "ProjectAnalyzer"]

import os
import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from ai_helpers import enhance_readme_with_ai


class ProjectAnalyzer:
    """Analyzes project structure and extracts relevant information."""

    def __init__(self, project_path: Path, verbose: bool = False):
        self.project_path = project_path
        self.verbose = verbose
        self.ignore_patterns = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "venv",
            "node_modules",
            ".DS_Store",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            ".coverage",
            ".tox",
            ".mypy_cache",
            ".ruff_cache",
        }

    def get_project_name(self) -> str:
        """Extract project name from directory name."""
        return self.project_path.name

    def _categorize_file(self, file: str) -> str:
        """Categorize file by type."""
        if file.endswith(".py"):
            return "python_files"
        elif file.endswith((".js", ".ts", ".jsx", ".tsx")):
            return "javascript_files"
        elif file.endswith((".html", ".htm")):
            return "html_files"
        elif file.endswith((".css", ".scss", ".sass")):
            return "css_files"
        elif file.endswith((".json", ".yaml", ".yml", ".toml", ".ini", ".cfg")):
            return "config_files"
        elif file.endswith((".md", ".txt", ".rst")):
            return "documentation"
        else:
            return "other_files"

    def get_file_structure(self) -> Dict[str, List[str]]:
        """Get the project file structure, organized by file type."""
        structure = {
            "python_files": [],
            "javascript_files": [],
            "html_files": [],
            "css_files": [],
            "config_files": [],
            "documentation": [],
            "other_files": [],
        }

        for root, dirs, files in os.walk(self.project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]

            for file in files:
                if any(pattern in file for pattern in self.ignore_patterns):
                    continue

                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_path)
                category = self._categorize_file(file)
                structure[category].append(str(relative_path))

        return structure

    def get_dependencies(self) -> Dict[str, List[str]]:
        """Extract project dependencies from various files."""
        dependencies = {"python": [], "node": [], "other": []}

        # Check for Python dependencies
        requirements_files = [
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "Pipfile",
        ]
        for req_file in requirements_files:
            req_path = self.project_path / req_file
            if req_path.exists():
                if self.verbose:
                    print(f"Found requirements file: {req_file}")
                if req_file == "requirements.txt":
                    dependencies["python"] = self._parse_requirements_txt(req_path)
                elif req_file == "pyproject.toml":
                    dependencies["python"] = self._parse_pyproject_toml(req_path)
                break

        # Check for Node.js dependencies
        package_json = self.project_path / "package.json"
        if package_json.exists():
            if self.verbose:
                print("Found package.json")
            dependencies["node"] = self._parse_package_json(package_json)

        return dependencies

    def _parse_requirements_txt(self, file_path: Path) -> List[str]:
        """Parse requirements.txt file."""
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            deps = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Extract package name (remove version specifiers)
                    package = re.split(r"[<>=!~]", line)[0].strip()
                    deps.append(package)
            return deps
        except Exception as e:
            if self.verbose:
                print(f"Error parsing requirements.txt: {e}")
            return []

    def _parse_pyproject_toml(self, file_path: Path) -> List[str]:
        """Parse pyproject.toml file for dependencies."""
        try:
            # Try to import tomllib (Python 3.11+)
            import sys

            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib  # type: ignore[import]

            with open(file_path, "rb") as f:
                data = tomllib.load(f)

            deps = []
            if "project" in data and "dependencies" in data["project"]:
                for dep in data["project"]["dependencies"]:
                    package = re.split(r"[<>=!~]", dep)[0].strip()
                    deps.append(package)
            return deps
        except Exception as e:
            if self.verbose:
                print(f"Error parsing pyproject.toml: {e}")
            return []

    def _parse_package_json(self, file_path: Path) -> List[str]:
        """Parse package.json file for dependencies."""
        try:
            import json

            with open(file_path, "r") as f:
                data = json.load(f)

            deps = []
            if "dependencies" in data:
                deps.extend(data["dependencies"].keys())
            if "devDependencies" in data:
                deps.extend(data["devDependencies"].keys())
            return deps
        except Exception as e:
            if self.verbose:
                print(f"Error parsing package.json: {e}")
            return []

    def get_main_files(self) -> List[str]:
        """Identify main entry points for the project."""
        main_files = []

        # Common entry points
        entry_points = [
            "main.py",
            "app.py",
            "run.py",
            "server.py",
            "index.py",
            "index.js",
            "app.js",
            "server.js",
            "main.js",
            "index.html",
            "app.html",
        ]

        for entry in entry_points:
            if (self.project_path / entry).exists():
                main_files.append(entry)

        return main_files


def _generate_installation_section(
    dependencies: Dict[str, List[str]], file_structure: Dict[str, List[str]]
) -> str:
    """Generate installation section content."""
    content = "## Installation\n\n"

    if dependencies["python"]:
        content += "### Python Dependencies\n\n"
        content += "```bash\n"
        if any(
            file.endswith("requirements.txt") for file in file_structure["config_files"]
        ):
            content += "pip install -r requirements.txt\n"
        else:
            content += "pip install " + " ".join(dependencies["python"][:5]) + "\n"
        content += "```\n\n"

    if dependencies["node"]:
        content += "### Node.js Dependencies\n\n"
        content += "```bash\n"
        content += "npm install\n"
        content += "```\n\n"

    return content


def _generate_usage_section(main_files: List[str]) -> str:
    """Generate usage section content."""
    content = "## Usage\n\n"
    if main_files:
        content += "To run the project:\n\n"
        content += "```bash\n"
        if "main.py" in main_files:
            content += "python main.py\n"
        elif "app.py" in main_files:
            content += "python app.py\n"
        elif "index.js" in main_files:
            content += "node index.js\n"
        else:
            content += f"python {main_files[0]}\n"
        content += "```\n\n"
    else:
        content += "```bash\n"
        content += "# Add usage instructions here\n"
        content += "```\n\n"

    return content


def _generate_structure_section(file_structure: Dict[str, List[str]]) -> str:
    """Generate project structure section content."""
    content = "## Project Structure\n\n"
    content += "```\n"

    # Show top-level structure
    for category, files in file_structure.items():
        if files:
            content += f"{category.replace('_', ' ').title()}:\n"
            for file in sorted(files)[:10]:  # Limit to first 10 files
                content += f"  ├── {file}\n"
            if len(files) > 10:
                content += f"  └── ... and {len(files) - 10} more files\n"
            content += "\n"

    content += "```\n\n"
    return content


def _generate_dependencies_section(dependencies: Dict[str, List[str]]) -> str:
    """Generate dependencies section content."""
    if not any(dependencies.values()):
        return ""

    content = "## Dependencies\n\n"

    if dependencies["python"]:
        content += "### Python\n\n"
        for dep in dependencies["python"][:10]:  # Limit to first 10
            content += f"- {dep}\n"
        if len(dependencies["python"]) > 10:
            content += f"- ... and {len(dependencies['python']) - 10} more\n"
        content += "\n"

    if dependencies["node"]:
        content += "### Node.js\n\n"
        for dep in dependencies["node"][:10]:  # Limit to first 10
            content += f"- {dep}\n"
        if len(dependencies["node"]) > 10:
            content += f"- ... and {len(dependencies['node']) - 10} more\n"
        content += "\n"

    return content


def generate_readme(
    project_path: Path,
    output_file: str = "README.md",
    force_overwrite: bool = False,
    verbose: bool = False,
    use_ai_enhancement: bool = True,
) -> bool:
    """
    Generate a README file for the given project path.

    Args:
        project_path: Path to the project directory
        output_file: Name of the output README file
        force_overwrite: Whether to overwrite existing README
        verbose: Enable verbose output
        use_ai_enhancement: Whether to use AI to enhance the README

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if README already exists
        readme_path = project_path / output_file
        if readme_path.exists() and not force_overwrite:
            print(f"⚠️  README file already exists: {output_file}")
            print("Use --force to overwrite")
            return False

        if verbose:
            print(f"Starting README generation for: {project_path}")

        # Analyze the project
        analyzer = ProjectAnalyzer(project_path, verbose)
        project_name = analyzer.get_project_name()
        file_structure = analyzer.get_file_structure()
        dependencies = analyzer.get_dependencies()
        main_files = analyzer.get_main_files()

        if verbose:
            print(f"Project name: {project_name}")
            print(f"Main files found: {main_files}")

        # Generate the README content
        readme_content = _generate_readme_content(
            project_name=project_name,
            file_structure=file_structure,
            dependencies=dependencies,
            main_files=main_files,
            project_path=project_path,
        )

        # Enhance with AI if requested
        if use_ai_enhancement:
            if verbose:
                print("Enhancing README with AI...")
            try:
                readme_content = enhance_readme_with_ai(readme_content, project_path)
            except Exception as e:
                if verbose:
                    print(f"AI enhancement failed: {e}")
                # Continue with the basic README

        # Write the README file
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)

        if verbose:
            print(f"README written to: {readme_path}")

        return True

    except Exception as e:
        if verbose:
            print(f"Error generating README: {e}")
            import traceback

            traceback.print_exc()
        return False


def _generate_readme_content(
    project_name: str,
    file_structure: Dict[str, List[str]],
    dependencies: Dict[str, List[str]],
    main_files: List[str],
    project_path: Path,
) -> str:
    """Generate the README content based on project analysis."""

    # Project title
    content = f"# {project_name}\n\n"

    # Project description (placeholder)
    content += "## Description\n\n"
    content += "A brief description of what this project does and who it's for.\n\n"

    # Features
    content += "## Features\n\n"
    content += "- Feature 1\n"
    content += "- Feature 2\n"
    content += "- Feature 3\n\n"

    # Installation
    content += _generate_installation_section(dependencies, file_structure)

    # Usage
    content += _generate_usage_section(main_files)

    # Project Structure
    content += _generate_structure_section(file_structure)

    # Dependencies
    content += _generate_dependencies_section(dependencies)

    # Contributing
    content += "## Contributing\n\n"
    content += "Contributions are always welcome!\n\n"
    content += "1. Fork the project\n"
    content += (
        "2. Create your feature branch (`git checkout -b feature/AmazingFeature`)\n"
    )
    content += "3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)\n"
    content += "4. Push to the branch (`git push origin feature/AmazingFeature`)\n"
    content += "5. Open a Pull Request\n\n"

    # License
    content += "## License\n\n"
    content += "This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n\n"

    # Footer
    content += "---\n\n"
    content += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return content
