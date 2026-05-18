"""BFCL tool schemas.

Auto-generated from /ossfs/workspace/bfcl_xiexin/bfcl_eval/data/multi_turn_func_doc
"""

from .gorilla_file_system import GORILLA_FILE_SYSTEM_TOOL_SCHEMAS
from .math_api import MATH_API_TOOL_SCHEMAS
from .memory_kv import MEMORY_KV_TOOL_SCHEMAS
from .memory_rec_sum import MEMORY_REC_SUM_TOOL_SCHEMAS
from .memory_vector import MEMORY_VECTOR_TOOL_SCHEMAS
from .message_api import MESSAGE_API_TOOL_SCHEMAS
from .posting_api import POSTING_API_TOOL_SCHEMAS
from .ticket_api import TICKET_API_TOOL_SCHEMAS
from .trading_bot import TRADING_BOT_TOOL_SCHEMAS
from .travel_booking import TRAVEL_BOOKING_TOOL_SCHEMAS
from .vehicle_control import VEHICLE_CONTROL_TOOL_SCHEMAS
from .web_search import WEB_SEARCH_TOOL_SCHEMAS

__all__ = ["GORILLA_FILE_SYSTEM_TOOL_SCHEMAS", "MATH_API_TOOL_SCHEMAS", "MEMORY_KV_TOOL_SCHEMAS", "MEMORY_REC_SUM_TOOL_SCHEMAS", "MEMORY_VECTOR_TOOL_SCHEMAS", "MESSAGE_API_TOOL_SCHEMAS", "POSTING_API_TOOL_SCHEMAS", "TICKET_API_TOOL_SCHEMAS", "TRADING_BOT_TOOL_SCHEMAS", "TRAVEL_BOOKING_TOOL_SCHEMAS", "VEHICLE_CONTROL_TOOL_SCHEMAS", "WEB_SEARCH_TOOL_SCHEMAS"]

# Combined schemas for easy access
BFCL_ALL_SCHEMAS = {
    "gorilla_file_system": GORILLA_FILE_SYSTEM_TOOL_SCHEMAS,
    "math_api": MATH_API_TOOL_SCHEMAS,
    "memory_kv": MEMORY_KV_TOOL_SCHEMAS,
    "memory_rec_sum": MEMORY_REC_SUM_TOOL_SCHEMAS,
    "memory_vector": MEMORY_VECTOR_TOOL_SCHEMAS,
    "message_api": MESSAGE_API_TOOL_SCHEMAS,
    "posting_api": POSTING_API_TOOL_SCHEMAS,
    "ticket_api": TICKET_API_TOOL_SCHEMAS,
    "trading_bot": TRADING_BOT_TOOL_SCHEMAS,
    "travel_booking": TRAVEL_BOOKING_TOOL_SCHEMAS,
    "vehicle_control": VEHICLE_CONTROL_TOOL_SCHEMAS,
    "web_search": WEB_SEARCH_TOOL_SCHEMAS,
}
