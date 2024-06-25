from pssim.interfaces.memory import IMemory
from pssim.modules.config import mem_config as config  


class Memory(IMemory):
    _size: int = config["size"]
    _free: int = config["size"]

    @property
    def size(self) -> int:
        return self._size

    @property
    def free(self) -> int:
        return self._free
