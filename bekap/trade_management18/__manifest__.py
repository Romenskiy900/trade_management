{
    "name": "Trade management",
    "version": "1.0",
    "depends": ["base", "stock", "product"],

    "data": [
        "data/sequence.xml",

        "security/trade_management_groups.xml",
        "security/trade_management_security.xml",
        "security/ir.model.access.csv",


        "views/product_views.xml",
        "views/res_partner_view.xml",
        "views/trade_management_actions.xml",


        "views/trade_management_sales_views.xml",
        "views/trade_management_price_set_views.xml",
        "views/trade_management_receipt_views.xml",
        "views/sales_pivot.xml",
        "views/price_set_line_graph.xml",

        "views/wizard_product_category_views.xml",

        "views/receipt_report_wizard.xml",

        "report/receipt_report.xml",
        "report/receipt_report_templates.xml",

        "views/trade_management_menu.xml",
    ],

    "demo": [
        "demo/product_category_demo.xml",
        "demo/demo_product.xml",
        "demo/demo_price_set.xml",
        "demo/demo_res_partner.xml",
        "demo/demo_receipt.xml",
        "demo/demo_sales.xml",

    ],

    'post_init_hook': 'post_init_hook',

    'test': [
        'tests/test_price_set.py',
    ],

    "installable": True,
    "application": True
}