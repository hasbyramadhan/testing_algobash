from odoo import http
from odoo.http import request

class RoomBookingAPI(http.Controller):

    def _validate_token(self, token):
        valid_token = "your_secure_token"  # Ganti dengan token yang sesuai
        if token != valid_token:
            return False
        return True

    @http.route('/api/booking_status/<int:booking_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_booking_status(self, booking_id, **kwargs):
        token = request.httprequest.headers.get('Authorization')
        
        if not token or not self._validate_token(token.split(" ")[-1]):
            return {"error": "Unauthorized"}, 401

        booking = request.env['pemesanan.ruangan'].sudo().search([('id', '=', booking_id)], limit=1)
        
        if not booking:
            return {"error": "Booking not found"}, 404

        return {
            "booking_id": booking.id,
            "nomor_pemesanan": booking.nomor_pemesanan,
            "ruangan": booking.ruangan_id.nama_ruangan,
            "nama_pemesan": booking.nama_pemesan,
            "tanggal_pemesanan": booking.tanggal_pemesanan,
            "status_pemesanan": booking.status_pemesanan,
        }
        print("tes")
