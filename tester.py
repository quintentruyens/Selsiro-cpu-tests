"""
Provides the abstract Tester class which can be used to test an implementation of the CPU
"""

from abc import ABC, abstractmethod


class Tester(ABC):
    """Defines the interface to an implementation of the CPU for testing"""

    @abstractmethod
    def start(self, program: bytes) -> None:
        """Start the CPU with the given program"""

    @abstractmethod
    def stop(self) -> None:
        """Stop the CPU"""

    @abstractmethod
    def clock(self) -> None:
        """Execute one instruction on the CPU"""

    @abstractmethod
    def get_pc(self) -> int:
        """Get the current program counter"""

    @abstractmethod
    def get_register(self, reg_num: int) -> int:
        """Get the value of register reg_num"""

    @abstractmethod
    def read_memory(self, address: int) -> int:
        """Get the value stored at the given address"""
