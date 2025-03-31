# -*- coding: utf-8 -*-

from odoo import fields, http, models, _, api
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.account.controllers.download_docs import _get_headers, _build_zip_from_data
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)




class SaleOrder(models.Model):
    _inherit = "sale.order"


    def _get_name_portal_content_view(self):
        self.ensure_one()
        #return 'custom_portal_preview_report.report_order_document_mct_abonnement' if self.is_subscription else super()._get_name_portal_content_view()
        return 'custom_portal_preview_report.report_portal_abonnement'



class PortalAccount(CustomerPortal):

    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type == 'pdf' and download and invoice_sudo.state == 'posted':

            _logger.info('******************** if 1')

            # Download the official attachment(s) or a Pro Forma invoice
            docs_data = invoice_sudo._get_invoice_legal_documents_all(allow_fallback=True)
            if len(docs_data) == 1:
                headers = self._get_http_headers(invoice_sudo, report_type, docs_data[0]['content'], download)
                return request.make_response(docs_data[0]['content'], list(headers.items()))
            else:
                filename = invoice_sudo._get_invoice_report_filename(extension='zip')
                zip_content = _build_zip_from_data(docs_data)
                headers = _get_headers(filename, 'zip', zip_content)
                return request.make_response(zip_content, headers)

        elif report_type in ('html', 'pdf', 'text'):
            _logger.info('******************** elif 1')
            has_generated_invoice = bool(invoice_sudo.invoice_pdf_report_id)
            request.update_context(proforma_invoice=not has_generated_invoice)
            # Use the template set on the related partner if there is.
            # This is not perfect as the invoice can still have been computed with another template, but it's a slight fix/imp for stable.

            # if invoice_sudo.invoice_origin:
            #     _logger.info('************** invoice_sudo.invoice_origin %s', invoice_sudo.invoice_origin)
            #     abonnement = request.env['sale.order'].search([('name', '=', invoice_sudo.invoice_origin)])
            #     if abonnement:
            #
            #         # report = request.env['ir.actions.report'].search([('id', '=', 661)])
            #         report = request.env.ref('custom_portal_preview_report.account_invoices_mct_portal_preview')
            #         pdf_report_name = report.report_name
            #     else:
            #         _logger.info('************** else 1')
            #         pdf_report_name = 'account.account_invoices'
            #
            #
            # else:
            #     _logger.info('************** else 2')
            pdf_report_name = 'custom_portal_preview_report.account_invoices_mct_portal_preview'
            # report = request.env.ref('custom_portal_preview_report.account_invoices_mct_portal_preview')
            # pdf_report_name = report.report_name
            return self._show_report(model=invoice_sudo, report_type=report_type, report_ref=pdf_report_name,
                                     download=download)

        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        return request.render("account.portal_invoice_page", values)


