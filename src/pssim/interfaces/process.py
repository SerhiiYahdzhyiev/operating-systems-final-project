from abc import ABC, abstractmethod


class IProcess(ABC):
  @abstractmethod
  def wait(self, time: int):
    raise NotImplementedError

  @abstractmethod
  def execute(self, time: int = 1):
    raise NotImplementedError

  @abstractmethod
  def set_ready(self):
    raise NotImplementedError

  @abstractmethod
  def set_waiting(self):
    raise NotImplementedError

  @property
  @abstractmethod
  def finished(self) -> bool:
    raise NotImplementedError

  @property
  @abstractmethod
  def waiting_time(self) -> int:
    raise NotImplementedError

  @property
  @abstractmethod
  def service_time(self) -> int:
    raise NotImplementedError
