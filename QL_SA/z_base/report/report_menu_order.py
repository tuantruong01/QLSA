from odoo import api, fields, models


class ReportMenuOrder(models.AbstractModel):
    _name = 'report.report_menu_order'
    _inherit = "report.report_xlsx.abstract"
    _description = 'Bao cao thuc don da dat'

    def generate_xlsx_report(self, workbook, data, records):
        name = "Sheet"
        ws = workbook.add_worksheet(name)

        sql = f"""
             select cd.name ,cd.employee_id, hd.name phong_ban, cd.date_register, cd.ate 
             from confirm_dish cd
             left join hr_department hd on cd.department = hd.id 
                where cd.date_register::date between '{records.begin}' and '{records.end}'
                    AND cd.company_id = {self.env.company.id}
             ORDER BY cd.date_register

        """
        self.env.cr.execute(sql)
        datas = self.env.cr.dictfetchall()
        header = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': 'Times New Roman',
            'font_size': 16
        })
        table_header = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#DDEBF6',
            'border': 1,
            'font_name': 'Times New Roman',
            'font_size': 13
        })
        table_content = workbook.add_format({
            'bold': 0,
            'text_wrap': 1,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_name': 'Times New Roman',
            'font_size': 11
        })
        table_left = workbook.add_format({
            'bold': 0,
            'text_wrap': 1,
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'font_name': 'Times New Roman',
            'font_size': 11
        })
        header_content = workbook.add_format({
            'bold': 1,
            'text_wrap': 1,
            'align': 'left',
            'valign': 'vcenter',
            'font_name': 'Times New Roman',
            'font_size': 11,
            'italic': 1
        })
        ws.set_column(0, 0, 7)
        ws.set_column(1, 1, 10)
        ws.set_column(2, 2, 15)
        ws.set_column(3, 3, 15)
        ws.set_column(4, 4, 10)
        row = 0
        ws.merge_range(row, 0, row, 5, 'BÁO CÁO THỰC ĐƠN ĐÃ ĐẶT', header)
        row += 1
        ws.merge_range(row, 0, row, 5,
                       f'Từ ngày: {records.begin.strftime("%d-%m-%Y")} đến {records.end.strftime("%d-%m-%Y")}',
                       header_content)
        row += 1
        ws.write(row, 0, "STT", table_header)
        ws.write(row, 1, "Tên phiếu", table_header)
        ws.write(row, 2, "Người đăng lý", table_header)
        ws.write(row, 3, "Phòng ban", table_header)
        ws.write(row, 4, "Ngày đăng ký", table_header)
        ws.write(row, 5, "Tình trạng", table_header)
        row += 1
        stt = 1
        for data in datas:
            check = ''
            if data.get('ate'):
                check = 'Đã ăn'
            else:
                check = 'Chưa ăn'
            ws.write(row, 0, stt, table_content)
            ws.write(row, 1, data.get('name', ''), table_left)
            ws.write(row, 2, data.get('employee_id', ''), table_left)
            ws.write(row, 3, data.get('phong_ban', ''), table_left)
            ws.write(row, 4, data.get('date_register', '').strftime("%d-%m-%Y"), table_content)
            ws.write(row, 5, check, table_left)
            row += 1
            stt += 1
