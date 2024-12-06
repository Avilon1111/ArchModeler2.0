from Database.DbConnections import ArchModelInfoDb, ArchModelGraphDb
from Database.config import *

archModelGraphDb = ArchModelGraphDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_GRAPH_DB_NAME)
archModelInfoDb = ArchModelInfoDb(HOST, ROOT_USERNAME, ROOT_PASSWORD, MODEL_INFO_DB_NAME)
