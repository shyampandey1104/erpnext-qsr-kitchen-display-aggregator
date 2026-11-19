import unittest
from qsr_kitchen_aggregator.engine import KitchenOrderItem, UnifiedKitchenTicket, QSRKitchenAggregatorEngine

class TestQSRKitchenAggregatorEngine(unittest.TestCase):
    def setUp(self):
        self.kds = QSRKitchenAggregatorEngine("BurgerCrafters Cloud Kitchen")

    def test_order_ingestion_and_station_routing(self):
        items = [
            KitchenOrderItem("BURGER-CHEESE", "Double Smash Cheeseburger", 2, "GRILL", 6),
            KitchenOrderItem("PERI-FRIES", "Peri Peri Crispy Fries", 2, "FRYER", 4),
            KitchenOrderItem("SHAKE-CHOC", "Belgian Chocolate Shake", 1, "BEVERAGE", 3)
        ]
        ticket = UnifiedKitchenTicket(
            ticket_id="KDS-TICK-9901", channel_source="SWIGGY", channel_order_id="SWIG-981240",
            items=items, created_at="2026-03-01T19:30:00"
        )
        self.kds.ingest_channel_order(ticket)

        # Check grill station
        grill = self.kds.route_station_items("GRILL")
        self.assertEqual(len(grill), 1)
        self.assertEqual(grill[0]["item_name"], "Double Smash Cheeseburger")

        # Ready for dispatch
        res = self.kds.mark_ticket_ready_for_dispatch("KDS-TICK-9901")
        self.assertEqual(res["status"], "READY_FOR_DISPATCH")
        self.assertTrue(res["notify_delivery_rider"])

if __name__ == "__main__":
    unittest.main()
