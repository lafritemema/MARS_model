
# from mars.equipment import Equipment as EQUIPMENT
# from mars.reference import Reference as REFERENCE
# from mars.register import COMMAND_REGISTER as COMMAND_REGISTER
# from db.exceptions import DBDriverException
# from exceptions import BaseException
# from mars import MARS_DB_DRIVER as DB_DRIVER

from model.equipment import EquipmentI
from model.reference import ReferenceI


DB_DRIVER = object()
COMMAND_REGISTER = object()
EQUIPMENT:EquipmentI = object()
REFERENCE:ReferenceI = object()