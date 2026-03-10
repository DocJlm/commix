"""
Git utilities for commix.
"""
import subprocess
import os
from pathlib import Path
from typing import Optional


class GitUtils:
    """Git operations helper."""

    @staticmethod
    def is_git_repo() -> bool:
        """Check if current directory is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def get_diff(staged_only: bool = False, file_filter: Optional[str] = None) -> str:
        """Get git diff output."""
        try:
            cmd = ["git", "diff"]
            if staged_only:
                cmd.append("--staged")
            cmd.append("--no-color")

            if file_filter:
                cmd.extend(["--", file_filter])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=os.getcwd(),
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def get_staged_files() -> list[str]:
        """Get list of staged files."""
        try:
            result = subprocess.run(
                ["git", "diff", "--staged", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []

    @staticmethod
    def get_status() -> str:
        """Get git status output."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def commit(message: str, amend: bool = False) -> bool:
        """Create a git commit."""
        try:
            cmd = ["git", "commit"]
            if amend:
                cmd.append("--amend")
            cmd.extend(["-m", message])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=os.getcwd(),
            )
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"Error committing: {e.stderr}")
            return False

    @staticmethod
    def get_branch() -> str:
        """Get current branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def add(files: list[str] = None) -> bool:
        """Stage files for commit."""
        try:
            cmd = ["git", "add"]
            if files:
                cmd.extend(files)
            else:
                cmd.append(".")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=os.getcwd(),
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def has_staged_changes() -> bool:
        """Check if there are staged changes."""
        try:
            result = subprocess.run(
                ["git", "diff", "--staged", "--quiet"],
                capture_output=True,
                check=True,
            )
            return result.returncode != 0
        except subprocess.CalledProcessError:
            return True

    @staticmethod
    def get_commit_history(count: int = 10) -> list[str]:
        """Get recent commit messages."""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--pretty=format:%s"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []

    @staticmethod
    def get_repo_info() -> dict:
        """Get repository information."""
        return {
            "branch": GitUtils.get_branch(),
            "root": GitUtils.get_repo_root(),
            "has_changes": bool(GitUtils.get_status().strip()),
            "has_staged": GitUtils.has_staged_changes(),
        }

    @staticmethod
    def get_repo_root() -> str:
        """Get repository root directory."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
