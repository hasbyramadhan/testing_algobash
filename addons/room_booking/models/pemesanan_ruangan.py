from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class PemesananRuangan(models.Model):
    _name = 'pemesanan.ruangan'
    _description = 'Pemesanan Ruangan'

    nomor_pemesanan = fields.Char(string='Nomor Pemesanan', required=True, copy=False, readonly=True, default=lambda self: 'New')
    ruangan_id = fields.Many2one('master.ruangan', string='Ruangan', required=True)
    nama_pemesan = fields.Char(string='Nama Pemesan', required=True)
    tanggal_pemesanan = fields.Date(string='Tanggal Pemesanan', required=True)
    status_pemesanan = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'On Going'),
        ('done', 'Done')
    ], string='Status Pemesanan', default='draft')
    catatan_pemesanan = fields.Text(string='Catatan Pemesanan')

    # Generate nomor pemesanan secara otomatis
    @api.model
    def create(self, vals):
        # Dapatkan sequence pemesanan
        if vals.get('nomor_pemesanan', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('pemesanan.ruangan') or 'New'

            # Dapatkan data tipe ruangan dari master ruangan
            ruangan = self.env['master.ruangan'].browse(vals['ruangan_id'])

            # Ambil tipe ruangan
            tipe_ruangan = ruangan.tipe_ruangan

            # Format tanggal (YYYYMMDD)
            tanggal_pemesanan = vals.get('tanggal_pemesanan', datetime.today().strftime('%Y-%m-%d'))
            tanggal_formatted = datetime.strptime(tanggal_pemesanan, '%Y-%m-%d').strftime('%Y%m%d')

            # Gabungkan semua elemen menjadi satu nomor pemesanan
            vals['nomor_pemesanan'] = f'PMSN-{tipe_ruangan.upper()}-{tanggal_formatted}-{sequence}'

        return super(PemesananRuangan, self).create(vals)



    # Validasi untuk ruangan yang sama pada tanggal yang sama
    @api.constrains('ruangan_id', 'tanggal_pemesanan')
    def _check_unique_booking(self):
        for record in self:
            existing_booking = self.search([
                ('ruangan_id', '=', record.ruangan_id.id),
                ('tanggal_pemesanan', '=', record.tanggal_pemesanan),
                ('id', '!=', record.id)
            ])
            if existing_booking:
                raise ValidationError("Ruangan sudah dipesan untuk tanggal ini.")

    # Validasi untuk nama pemesan unik
    @api.constrains('nama_pemesan')
    def _check_unique_name(self):
        for record in self:
            if self.search([('nama_pemesan', '=', record.nama_pemesan), ('id', '!=', record.id)]):
                raise ValidationError("Nama Pemesan sudah digunakan.")

    # Fungsi untuk Set On Going
    def action_set_ongoing(self):
        for record in self:
            if record.status_pemesanan != 'draft':
                raise ValidationError("Hanya pemesanan dengan status Draft yang bisa diubah ke On Going.")
            record.status_pemesanan = 'ongoing'

    # Fungsi untuk Set Done
    def action_set_done(self):
        for record in self:
            if record.status_pemesanan != 'ongoing':
                raise ValidationError("Hanya pemesanan dengan status On Going yang bisa diubah ke Done.")
            record.status_pemesanan = 'done'
