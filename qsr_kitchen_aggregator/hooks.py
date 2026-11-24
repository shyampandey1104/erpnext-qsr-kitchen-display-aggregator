# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "qsr_kitchen_aggregator"
app_title = "Erpnext Qsr Kitchen Display Aggregator"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Qsr Kitchen Display Aggregator - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/qsr_kitchen_aggregator/css/qsr_kitchen_aggregator.bundle.css"
app_include_js = "/assets/qsr_kitchen_aggregator/js/qsr_kitchen_aggregator.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Qsr Kitchen Display Aggregator Entry": {
        "validate": "qsr_kitchen_aggregator.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "qsr_kitchen_aggregator.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "qsr_kitchen_aggregator.tasks.hourly_sync"
    ],
    "daily": [
        "qsr_kitchen_aggregator.tasks.daily_reconciliation"
    ],
    "weekly": [
        "qsr_kitchen_aggregator.tasks.weekly_digest"
    ]
}
