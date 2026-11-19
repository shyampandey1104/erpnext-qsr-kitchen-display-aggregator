# ERPNext QSR Multi-Channel Order Aggregator & Kitchen Display System (KDS)

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![ERPNext POS](https://img.shields.io/badge/ERPNext-Point%20of%20Sale-orange.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

Multi-brand cloud kitchens and Quick Service Restaurant (QSR) chains operate in high-pressure environments fulfilling hundreds of tickets per hour from diverse channels: **Swiggy, Zomato, Dine-In POS, and Brand Direct Web Apps**.

Operational friction includes:
1. **Multiple Tablet Chaos:** Line cooks must watch 4 different delivery tablets, leading to missed orders and delayed prep times.
2. **Station Routing Bottlenecks:** Orders containing items from different stations (Grill, Deep Fryer, Assembly, Beverage) are not parsed intelligently, causing cold food dispatch.
3. **Delivery SLA Breaches:** Delivery aggregator algorithms penalize restaurants when kitchen prep exceeds promised target SLAs (typically 12–15 mins).

This Frappe application serves as an omnichannel KDS aggregator, synchronizing multi-channel orders into unified kitchen station touchscreens with real-time countdown timers.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["Swiggy / Zomato API Webhook"] -->|Inward Order JSON| B["Unified KDS Ingestion Engine"]
    C["Dine-In POS / Web Storefront"] --> B
    B -->|Generate Unified Kitchen Ticket| D["Master KDS Controller"]
    D -->|Item Decomposition & Station Routing| E["Kitchen Station Displays"]
    E -->|Grill Items (e.g. Burgers)| F["Grill Station Display"]
    E -->|Fryer Items (e.g. Fries)| G["Fryer Station Display"]
    E -->|Drinks / Desserts| H["Beverage Station Display"]
    F & G & H -->|Station Chefs Mark Ready| I["Expo / Assembly Table"]
    I -->|Pack & Seal Ticket| J["Order Ready: Notify Delivery Rider"]
    J -->|Close Ticket| K["ERPNext Sales Invoice & Inventory Depletion"]
```

---

## 🚀 Key Engineering Capabilities

- **Omnichannel Order Normalization:** Ingests orders from Swiggy, Zomato, DotPe, and ERPNext POS into a single format.
- **Intelligent Station Routing:** Routes individual ticket items to specialized prep stations (Grill, Pizza Oven, Fryer, Salad).
- **Live SLA Countdown Matrix:** Color-codes orders (Green $\rightarrow$ Amber $\rightarrow$ Red) based on elapsed prep time.
- **Real-Time Rider Notification:** Dispatches ready pings to delivery aggregator fleets the moment the expo station marks completion.

---

## 📂 Frappe DocType Schema & Data Structure

```text
qsr_kitchen_aggregator/
├── qsr_kitchen_aggregator_core/
│   ├── doctype/
│   │   ├── kds_unified_ticket/
│   │   │   ├── kds_unified_ticket.json
│   │   │   ├── kds_unified_ticket.py
│   │   │   └── kds_unified_ticket.js
│   │   └── kds_station_route/
│   │       └── kds_station_route.json
│   └── workspace/
│       └── qsr_kitchen_aggregator_workspace/
│           └── qsr_kitchen_aggregator_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/qsr_kitchen_aggregator.api.ingest_channel_order`
- **Whitelisted Method:** `@frappe.whitelist() def mark_ticket_ready_for_dispatch(ticket_id)`
- **Hooks Event:** `on_submit` of `POS Invoice` auto-spawns KDS tickets.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/erpnext-qsr-kitchen-display-aggregator
bench --site erp.yourdomain.com install-app qsr_kitchen_aggregator
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Optimized for Cloud Kitchens, Multi-Outlet QSRs, and Casual Dining Chains.
