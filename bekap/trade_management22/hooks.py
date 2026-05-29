from odoo import SUPERUSER_ID, api

def post_init_hook(env):
    # Создаем среду суперпользователя И передаем туда наш кастомный контекст
    ctx = {'install_demo': True}
    env = api.Environment(env.cr, SUPERUSER_ID, ctx)

    # Передаем этот контекст в методы выполнения
    receipts = env['trade.management.receipt'].search([])
    receipts.with_context(install_demo=True).action_post()

    sales = env['trade.management.sales'].search([])
    sales.with_context(install_demo=True).action_post()