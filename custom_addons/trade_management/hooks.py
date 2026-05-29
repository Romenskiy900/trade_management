from odoo import SUPERUSER_ID, api


def post_init_hook(env):
    # create superuser environment with custom installation context
    ctx = {'install_demo': True}
    env = api.Environment(env.cr, SUPERUSER_ID, ctx)

    # automatically post all receipts after module installation
    receipts = env['trade.management.receipt'].search([])
    receipts.with_context(install_demo=True).action_post()

    # automatically post all sales after module installation
    sales = env['trade.management.sales'].search([])
    sales.with_context(install_demo=True).action_post()