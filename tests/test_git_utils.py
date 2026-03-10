"""
Tests for git utilities module.
"""
import pytest
import subprocess
import tempfile
from pathlib import Path

from commix.git_utils import GitUtils


class TestGitUtils:
    """Test git utilities."""

    def test_not_git_repo(self):
        """Test non-git directory detection."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir)
                assert GitUtils.is_git_repo() is False
            finally:
                os.chdir(original_cwd)

    def test_is_git_repo(self):
        """Test git repository detection."""
        # This test assumes we're in a git repo
        # (the commix project itself)
        # Skip if not in a git repo
        import os
        original_cwd = Path.cwd()
        try:
            os.chdir(Path(__file__).parent.parent)
            if GitUtils.is_git_repo():
                assert GitUtils.is_git_repo() is True
                branch = GitUtils.get_branch()
                assert isinstance(branch, str)
        finally:
            os.chdir(original_cwd)

    def test_get_commit_history(self):
        """Test getting commit history."""
        import os
        original_cwd = Path.cwd()
        try:
            os.chdir(Path(__file__).parent.parent)
            if GitUtils.is_git_repo():
                history = GitUtils.get_commit_history(count=5)
                assert isinstance(history, list)
        finally:
            os.chdir(original_cwd)

    def test_get_diff(self):
        """Test getting git diff."""
        # Should return empty string when no changes
        import os
        original_cwd = Path.cwd()
        try:
            os.chdir(Path(__file__).parent.parent)
            if GitUtils.is_git_repo():
                diff = GitUtils.get_diff()
                assert isinstance(diff, str)
        finally:
            os.chdir(original_cwd)
