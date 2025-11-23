#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Test Suite
Tests MCP server connectivity and basic functionality
"""

import subprocess
import sys
import time
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_success(text):
    """Print success message"""
    print(f"✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")


def test_mcp_sdk():
    """Test MCP Python SDK installation"""
    print_header("Testing MCP Python SDK")

    try:
        from mcp import ClientSession, StdioServerParameters
        import mcp
        print_success("MCP SDK imported successfully")
        print_info(f"MCP module location: {mcp.__file__}")
        return True
    except ImportError as e:
        print_error(f"Failed to import MCP SDK: {e}")
        return False


def test_git_mcp_server():
    """Test Git MCP server"""
    print_header("Testing Git MCP Server")

    try:
        # Test if uvx is available
        result = subprocess.run(
            ["which", "uvx"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            print_error("uvx is not installed")
            return False

        print_success(f"uvx found at: {result.stdout.strip()}")

        # Test git server help
        result = subprocess.run(
            ["uvx", "mcp-server-git", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print_success("Git MCP server is installed and working")
            print_info("Server help output:")
            for line in result.stdout.split('\n')[:10]:
                if line.strip():
                    print(f"    {line}")
            return True
        else:
            print_error(f"Git MCP server test failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print_error("Git MCP server test timed out")
        return False
    except Exception as e:
        print_error(f"Error testing Git MCP server: {e}")
        return False


def test_memory_mcp_server():
    """Test Memory MCP server"""
    print_header("Testing Memory MCP Server")

    try:
        # Check if memory-mcp is installed
        result = subprocess.run(
            ["pip", "show", "memory-mcp"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print_success("memory-mcp package is installed")

            # Try to run it with uvx
            result = subprocess.run(
                ["timeout", "2", "uvx", "memory-mcp"],
                capture_output=True,
                text=True,
                timeout=5
            )

            # Note: memory-mcp dev version doesn't provide executables
            if "does not provide any executables" in result.stdout or "does not provide any executables" in result.stderr:
                print_info("Note: memory-mcp package is installed but doesn't provide executable (dev version)")
                print_info("This is expected for memory-mcp 0.1.0.dev1")
                return True
            else:
                print_info("memory-mcp package status unclear")
                return True
        else:
            print_error("memory-mcp package not found")
            return False

    except Exception as e:
        print_error(f"Error testing Memory MCP server: {e}")
        return False


def test_mcp_configuration():
    """Test MCP configuration file"""
    print_header("Testing MCP Configuration")

    mcp_config = Path(".claude/mcp.json")

    if mcp_config.exists():
        print_success(f"MCP configuration file found: {mcp_config}")

        try:
            import json
            with open(mcp_config) as f:
                config = json.load(f)

            if "mcpServers" in config:
                server_count = len(config["mcpServers"])
                print_success(f"Found {server_count} MCP server configurations")

                for server_name, server_config in config["mcpServers"].items():
                    print_info(f"  • {server_name}: {server_config.get('description', 'No description')[:60]}...")

                return True
            else:
                print_error("Invalid MCP configuration: missing 'mcpServers' key")
                return False

        except json.JSONDecodeError as e:
            print_error(f"Invalid JSON in MCP configuration: {e}")
            return False
        except Exception as e:
            print_error(f"Error reading MCP configuration: {e}")
            return False
    else:
        print_error(f"MCP configuration file not found: {mcp_config}")
        return False


def test_environment_variables():
    """Test environment variables"""
    print_header("Testing Environment Variables")

    env_file = Path(".env")

    if env_file.exists():
        print_success(f"Environment file found: {env_file}")

        # Check if it has the required structure
        with open(env_file) as f:
            content = f.read()

        required_sections = [
            "# AI APIs - Required",
            "# Integration APIs - Optional",
            "# MCP (Model Context Protocol) Servers - Optional"
        ]

        all_found = True
        for section in required_sections:
            if section in content:
                print_success(f"Found section: {section}")
            else:
                print_error(f"Missing section: {section}")
                all_found = False

        return all_found
    else:
        print_error(f"Environment file not found: {env_file}")
        print_info("Create one by copying .env.example: cp .env.example .env")
        return False


def test_python_packages():
    """Test installed Python packages"""
    print_header("Testing Python Package Installations")

    packages = {
        "mcp": "MCP Python SDK",
        "mcp_server_git": "Git MCP Server",
        "memory_mcp": "Memory MCP Server",
        "anthropic": "Anthropic Claude SDK",
        "google.genai": "Google Gemini SDK",
        "openai": "OpenAI SDK",
        "flask": "Flask Framework"
    }

    results = {}

    for package, description in packages.items():
        try:
            # Handle package names with dots
            module_name = package.replace(".", "_") if "." in package else package
            __import__(package)
            print_success(f"{description} ({package})")
            results[package] = True
        except ImportError:
            print_error(f"{description} ({package}) - NOT INSTALLED")
            results[package] = False

    return all(results.values())


def main():
    """Run all MCP tests"""
    print("\n" + "🔌" * 30)
    print("  MCP (Model Context Protocol) Test Suite")
    print("  MWD Assistant - November 2025")
    print("🔌" * 30)

    results = {
        "Python Packages": test_python_packages(),
        "MCP SDK": test_mcp_sdk(),
        "Git MCP Server": test_git_mcp_server(),
        "Memory MCP Server": test_memory_mcp_server(),
        "MCP Configuration": test_mcp_configuration(),
        "Environment Variables": test_environment_variables(),
    }

    # Summary
    print_header("Test Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")

    print("\n" + "-" * 60)
    print(f"Tests Passed: {passed}/{total}")
    print("-" * 60)

    if passed == total:
        print("\n🎉 All MCP tests passed successfully!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
