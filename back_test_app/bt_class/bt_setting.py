#from constant_database_data import *
from .constant_database_data import *
from .my_database_info import get_database_info, website_data, vps1_local_access, laptop_local_access, vps1_remote_access

bt_database_info = get_database_info(pc_name=vps1_remote_access, database_name=website_data)
# bt_database_info = get_database_info(pc_name=vps1_local_access, database_name=website_data)
#bt_database_info = laptop_analyze_server_role_db_info
#bt_database_info = constant_database_data.laptop_analyze_server_role_db_info

