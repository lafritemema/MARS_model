from enum import Enum

class ReferenceI(Enum):
  @property
  def type(self)->str:
    return self.__class__.__name__.upper()
  @property
  def reference(self)->str:
    return self.value
