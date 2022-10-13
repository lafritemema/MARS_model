
from exceptions import BaseException

# TODO implement model exception
class ModelException(BaseException):
  def __init__(self, description:str, module:str):
    super()