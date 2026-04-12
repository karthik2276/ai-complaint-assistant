"""
Endee Vector Database
=====================
Lightweight file-backed vector store.
Mirrors the endee-io/endee public API.

Replace this directory with the real cloned repo:
    git clone https://github.com/endee-io/endee.git endee
"""

from .db import EndeeDB

__all__ = ["EndeeDB"]
__version__ = "0.1.0"
