"""Quick Service Restaurant (QSR) & Cloud Kitchen Display System (KDS) Aggregator."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class KitchenOrderItem:
    item_code: str
    item_name: str
    quantity: int
    station_routing: str    # GRILL, FRYER, ASSEMBLY, BEVERAGE
    cooking_time_mins: int

@dataclass
class UnifiedKitchenTicket:
    ticket_id: str
    channel_source: str     # SWIGGY, ZOMATO, DINE_IN_POS, WEB_DIRECT
    channel_order_id: str
    items: List[KitchenOrderItem]
    created_at: str
    sla_prep_target_mins: int = 15
    status: str = "RECEIVED" # RECEIVED, PREPARING, READY_FOR_DISPATCH, COMPLETED

class QSRKitchenAggregatorEngine:
    def __init__(self, brand_name: str):
        self.brand_name = brand_name
        self.tickets: Dict[str, UnifiedKitchenTicket] = {}

    def ingest_channel_order(self, ticket: UnifiedKitchenTicket) -> Dict[str, Any]:
        self.tickets[ticket.ticket_id] = ticket
        return {"ticket_id": ticket.ticket_id, "channel": ticket.channel_source, "items_count": len(ticket.items)}

    def route_station_items(self, station_name: str) -> List[Dict[str, Any]]:
        station_items = []
        for t in self.tickets.values():
            if t.status in ["RECEIVED", "PREPARING"]:
                for it in t.items:
                    if it.station_routing == station_name:
                        station_items.append({
                            "ticket_id": t.ticket_id,
                            "channel": t.channel_source,
                            "item_name": it.item_name,
                            "quantity": it.quantity,
                            "cooking_time_mins": it.cooking_time_mins
                        })
        return station_items

    def mark_ticket_ready_for_dispatch(self, ticket_id: str) -> Dict[str, Any]:
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found.")
        t = self.tickets[ticket_id]
        t.status = "READY_FOR_DISPATCH"
        return {"ticket_id": ticket_id, "status": t.status, "notify_delivery_rider": True}
