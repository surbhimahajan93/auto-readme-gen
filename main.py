#!/usr/bin/env python3
"""
Auto README Generator CLI

A command-line tool that automatically generates README files for projects
by analyzing the project structure and code.
"""

import argparse
import sys
from pathlib import Path

try:
    from generator import generate_readme
except ImportError:
    # Fallback for when running as script
    import generator

    generate_readme = generator.generate_readme


def validate_project_path(path):
    """Validate that the provided path exists and is a directory."""
    project_path = Path(path)
    if not project_path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {path}")
    if not project_path.is_dir():
        raise argparse.ArgumentTypeError(f"Path is not a directory: {path}")
    return project_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a README file for a project directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py /path/to/your/project
  python main.py . --output README.md
  python main.py /path/to/project --force
        """,
    )

    parser.add_argument(
        "project_path", type=validate_project_path, help="Path to the project directory"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="README.md",
        help="Output filename for the README (default: README.md)",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing README file if it exists",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    try:
        if args.verbose:
            print(f"Analyzing project at: {args.project_path}")
            print(f"Output file: {args.output}")

        # Generate the README
        success = generate_readme(
            project_path=args.project_path,
            output_file=args.output,
            force_overwrite=args.force,
            verbose=args.verbose,
        )

        if success:
            print(f"✅ README generated successfully: {args.output}")
            sys.exit(0)
        else:
            print("❌ Failed to generate README")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
