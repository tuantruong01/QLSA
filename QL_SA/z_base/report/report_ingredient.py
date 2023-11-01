from odoo import api, fields, models


class ReportIngredient(models.AbstractModel):
    _name = 'report.report_ingredient_xlsx'
    _inherit = "report.report_xlsx.abstract"
    _description = 'Báo cáo danh sách nguyên liệu'

    def generate_xlsx_report(self, workbook, data, records):
        name = "Sheet"
        ws = workbook.add_worksheet(name)

        sql = f"""
             SELECT pt.name, pt.categ_id, pt.list_price
             FROM product_template pt
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
        ws.set_column(0, 0, 30)
        ws.set_column(1, 1, 30)
        ws.set_column(2, 2, 30)
        ws.set_column(3, 3, 30)
        row = 0
        ws.merge_range(row, 0, row, 4, 'BÁO CÁO DANH SÁCH NGUYÊN LIỆU', header)

        row += 1
        ws.write(row, 0, "STT", table_header)
        ws.write(row, 1, "Tên Nguyên Liệu", table_header)
        ws.write(row, 2, "Nhóm Nguyên Liệu", table_header)
        ws.write(row, 3, "Giá Nguyên Liệu", table_header)
        row += 1
        total = 0
        for i in range(len(datas)):
            ws.write(row, 0, i + 1, table_content)
            ws.write(row, 1, datas[i]['name'], table_content)
            ws.write(row, 2, datas[i]['categ_id'], table_content)
            ws.write(row, 3, datas[i]['list_price'], table_content)
            total += datas[i]['list_price']
            row += 1

        ws.merge_range(row, 0, row, 3, total)
