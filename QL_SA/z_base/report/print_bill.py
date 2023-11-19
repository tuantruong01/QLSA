from odoo import api, fields, models


class PrintBillXlsx(models.AbstractModel):
    _name = 'report.print_bill_xlsx'
    _inherit = "report.report_xlsx.abstract"
    _description = 'In hóa đơn'

    def generate_xlsx_report(self, workbook, data, records):
        ws = workbook.add_worksheet()

        bold_center = workbook.add_format({
            'bold': True,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'top': 2,
            'left': 1,
            'right': 2,
            'bottom': 1
        })
        bold_center_1 = workbook.add_format({
            'bold': True,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11,
            'border': 1,
        })
        bold_center_3 = workbook.add_format({
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 9,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 2,
        })
        left_bold = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 11
        })
        left = workbook.add_format({
            'text_wrap': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 9,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 2,
        })
        right = workbook.add_format({
            'text_wrap': 1,
            'align': 'right',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'font_size': 9,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 2,
        })
        bold_right = workbook.add_format({
            'text_wrap': 1,
            'align': 'right',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'top': 1,
            'left': 1,
            'right': 2,
            'bottom': 2,
            'font_size': 9
        })
        bold_center_2 = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Calibri',
            'top': 1,
            'left': 1,
            'right': 2,
            'bottom': 1,
            'font_size': 9
        })
        today = fields.Date.today()
        row = 0
        ws.merge_range(row, 0, row, 3, f'Ngày in phiếu: {today.strftime("%d-%m-%Y")}')

        row += 1
        ws.merge_range(row, 0, row, 3, f'Mã hóa đơn: {records.name}')
        ws.merge_range(row, 4, row, 6, f'Thời gian bắt đầu: {records.start_day.strftime("%d/%m/%Y %H:%M:%S")}')

        row += 1
        ws.merge_range(row, 0, row, 3, f'Người đặt: {records.name_id.name}')
        ws.merge_range(row, 4, row, 6, f'Thời gian kết thúc: {records.end_day.strftime("%d/%m/%Y %H:%M:%S")}')

        row += 1
        ws.merge_range(row, 0, row, 3,
                       f'Kiểu Dịch Vụ: {dict(self.env["tigo.service"]._fields["type"].selection).get(records.type)}')
        ws.merge_range(row, 4, row, 6, f'Thời gian kết thúc: {records.time_use}')

        row += 1
        ws.merge_range(row, 0, row, 3, f'Phòng: {records.room_id.name}')
        ws.merge_range(row, 4, row, 6, f'Tiền phòng: {records.price} VNĐ')

        row += 1
        ws.merge_range(row, 0, row, 3, f'Tiền cọc: {records.deposit} VNĐ')

        row += 1

        ws.write(row, 0, "STT", bold_center_1)
        ws.merge_range(row, 1, row, 2, "Tên món", bold_center_1)
        ws.write(row, 3, "Số lượng", bold_center_1)
        ws.write(row, 4, "Đơn giá", bold_center_1)
        ws.write(row, 5, "Thành tiền", bold_center_1)
        ws.write(row, 6, "Ghi chú", bold_center_1)

        row += 1
        stt = 1
        for r in records.order_dish_ids:
            ws.write(row, 0, stt)
            ws.merge_range(row, 1, row, 2, r.dish_id.name if r.dish_id else '')
            ws.write(row, 3, r.number if r.number else 0)
            ws.write(row, 4, r.price_unit if r.price_unit else 0)
            ws.write(row, 5, r.price if r.price else 0)
            ws.write(row, 6, r.note if r.note else 0)
            stt += 1
            row += 1
        ws.merge_range(row, 0, row, 3, f'Tổng:')
        ws.merge_range(row, 4, row, 6, f'{records.total_price}')
