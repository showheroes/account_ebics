# Copyright 2009-2023 Noviat.
# License LGPL-3 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import fintech
    from fintech.ebics import EbicsKeyRing

    fintech.cryptolib = "cryptography"
except ImportError:
    _logger.warning("Failed to import fintech")


class EbicsChangePassphrase(models.TransientModel):
    _name = "ebics.change.passphrase"
    _description = "Change EBICS keys passphrase"

    ebics_userid_id = fields.Many2one(
        comodel_name="ebics.userid", string="EBICS UserID", readonly=True
    )
    old_pass = fields.Char(string="Old Passphrase", required=True)
    new_pass = fields.Char(string="New Passphrase", required=True)
    new_pass_check = fields.Char(string="New Passphrase (verification)", required=True)
    note = fields.Text(string="Notes", readonly=True)

    def change_passphrase(self):
        self.ensure_one()
        if (
            self.ebics_userid_id.ebics_passphrase_store
            and self.old_pass != self.ebics_userid_id.ebics_passphrase
        ):
            raise UserError(_("Incorrect old passphrase."))
        if self.new_pass != self.new_pass_check:
            raise UserError(_("New passphrase verification error."))
        if self.new_pass == self.ebics_userid_id.ebics_passphrase:
            raise UserError(_("New passphrase equal to old passphrase."))
        try:
            passphrase = (
                self.ebics_userid_id.ebics_passphrase_store
                and self.ebics_userid_id.ebics_passphrase
                or self.old_pass
            )
            keyring = EbicsKeyRing(
                keys=self.ebics_userid_id.ebics_keys_fn,
                passphrase=passphrase,
            )
            keyring.change_passphrase(self.new_pass)
        except ValueError as err:
            raise UserError(str(err)) from err
        self.ebics_userid_id.ebics_passphrase = self.new_pass
        self.note = "The EBICS Passphrase has been changed."

        module = __name__.split("addons.")[1].split(".")[0]
        result_view = self.env.ref(
            "%s.ebics_change_passphrase_view_form_result" % module
        )
        return {
            "name": _("EBICS Keys Change Passphrase"),
            "res_id": self.id,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "ebics.change.passphrase",
            "view_id": result_view.id,
            "target": "new",
            "type": "ir.actions.act_window",
        }

    def button_close(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window_close"}
