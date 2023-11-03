from odoo import api, fields, models


class ReportIngredient(models.AbstractModel):
    _name = 'report.report_ingredient_xlsx'
    _inherit = "report.report_xlsx.abstract"
    _description = 'Báo cáo danh sách nguyên liệu'

    def generate_xlsx_report(self, workbook, data, records):
        name = "Sheet"
        ws = workbook.add_worksheet(name)
        category = '1=1'
        if records.categ_ids:
            if len(records.categ_ids) > 1:
                category += ' and pt.categ_id in (' + ','.join(map(str, records.categ_ids.ids)) + ')'
            else:
                category += ' and pt.categ_id = ' + str(records.categ_ids.ids[0])
        else:
            category += ''

        sql = f"""
             SELECT pt.name as ten_nl, pc.name, pt.list_price
             FROM product_template pt
             Left join product_category pc on pc.id = pt.categ_id
             where {category}
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
        stt = 1
        total = 0
        for r in datas:
            ws.write(row, 0, stt, table_content)
            ws.write(row, 1, r.get('ten_nl', ''), table_content)
            ws.write(row, 2, r.get("name", ''), table_content)
            ws.write(row, 3, r.get("list_price", 0), table_content)
            if r['list_price']:
                total += r.get("list_price", 0)
            else:
                total += 0
            row += 1
            stt += 1

        ws.merge_range(row, 0, row, 3, total)
