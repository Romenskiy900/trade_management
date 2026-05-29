{
    "name": "Trade management",
    "version": "1.0",
    "depends": ["base"],
    "data": [
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/trade_management_counterparty_views.xml",
        "views/trade_management_sales_views.xml",
        "views/trade_management_price_set_views.xml",
        "views/trade_management_nomenclature_views.xml",
        "views/trade_management_nomenclature_type_views.xml",
        "views/trade_management_receipt_views.xml",
        "views/trade_management_sales_views.xml",
        "views/sales_pivot.xml",
        "views/trade_management_menu.xml",
     ],

    "demo": [
        "demo/demo_nomenclature_type.xml",
        "demo/demo_nomenclature.xml",
    ],

    "installable": True,
    "application": True
}