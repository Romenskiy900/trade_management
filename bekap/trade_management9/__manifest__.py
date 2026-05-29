{
    "name": "Trade management",
    "version": "1.0",
    # "depends": ["base"],
    "depends": ["base", "product"],
    "data": [
        "data/sequence.xml",
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/res_partner_view.xml",
        "views/trade_management_sales_views.xml",
        "views/trade_management_price_set_views.xml",
        "views/trade_management_receipt_views.xml",
        "views/trade_management_sales_views.xml",
        "views/sales_pivot.xml",
        "views/price_set_line_graph.xml",
        "views/wizard_product_category_views.xml",
        "report/receipt_report_views.xml",
        "report/receipt_report_templates.xml",
        # 'views/receipt_views.xml',
        # 'report/receipt_report.xml',
        # 'report/receipt_report_template.xml',
        "views/trade_management_menu.xml",


     ],

    "demo": [
        "demo/product_category_demo.xml",
        "demo/demo_product.xml",
    ],

    'i18n': [
        'i18n/uk.po',
    ],

    "installable": True,
    "application": True
}