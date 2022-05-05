
"""
 This is a script created for Krishna Garments for updating sales,
    Copyright (C) 2022  krishnagarments-dev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


# The Important things - citcode

import pyodbc

DBQ = 'D:\BESPOKE TSR\MData.mdb' #DB Location
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+DBQ+';')


def sale():
    cursor = conn.cursor()
    a = cursor.execute(f"SELECT ncompanycode,nusercode,nsaleno,dsaledate,ncustcode,nsaleamt,ncurrentpymnt,ntotdiscamt,njsno1,njsno2,ccustname,cab,ncashpaid,ncashbalancepaid,ccreatedtime,ceditedtime FROM salesmast ORDER BY nsaleno ASC;")
    sale_nos = []
    sale_amnts = []
    sale_dates = []
    discount_amounts = []
    creation_dates = []
    for i in cursor.fetchall():
        company_code = i[0]
        user_code = i[1]
        sale_no = i[2]
        sale_date = i[3]
        customer_code = i[4]
        sale_amnt = i[5]
        current_payment = i[6]
        discount_amount = i[7]
        journal_1 = i[8]
        journal_2 = i[9]
        customer_name = i[10]
        bill_type = i[11]
        cash_paid = i[12]
        balance_paid = i[13]
        creation_date = i[14]
        edited_date = i[15]
        sale_dates.append(sale_date)
        sale_nos.append(sale_no)
        sale_amnts.append(sale_amnt)
        discount_amounts.append(discount_amount)
        creation_dates.append(creation_date)
    cursor.close()
    return {"saledate":sale_dates,"billnumber":sale_nos,"saleamnt":sale_amnts,"discountamount":discount_amounts,"creationdate":creation_dates}
    return sale_dates,sale_nos,sale_amnts,discount_amounts,creation_dates
# sale() - This gives output in list - provides (sales date, bill numbers, bill amounts, discount amounts, creation dates)

def detailed_sale():
    sale_nos = []
    cit_codes = []
    bat_codes = []
    item_qtys = []
    price_lst = []
    cursor = conn.cursor()
    cursor.execute(f"SELECT nsaleno,citcode,citbatcode,nqty,nrate,ntax,nprice FROM salestran ORDER BY nsaleno ASC;")
    for i in cursor.fetchall():
        sale_nos.append(i[0])
        cit_codes.append(i[1])
        bat_codes.append(i[2])
        item_qtys.append(i[3])
        price_lst.append(i[4])

    cursor.close()
    return {"salenos":sale_nos,"citcode":cit_codes,"batcode":bat_codes,"itemqty":item_qtys,"pricelst":price_lst}
# detailed_sale() - This gives detailed list of products sold - provides (Bill Numbers, Citcodes , Batcodes, Quantity of Items, List Price of Products)

def list_product():
    cit_codes = []
    item_names = []
    item_units = []
    bat_codes = []
    sale_rates = []
    purchase_rates = []
    product_stock = []
    cursor = conn.cursor()
    cursor.execute(f"SELECT citcode,citname,cunit FROM item")
    for i in cursor.fetchall():
        citcode = i[0]
        cit_codes.append(i[0])
        item_names.append(i[1])
        item_units.append(i[2])
    for citcode in cit_codes:
        a = cursor.execute(f"SELECT citbatcode,nsalerate,nprrate,ncurstk FROM itembatch WHERE citcode='{citcode}'")
        b = a.fetchall()[0]
        bat_codes.append(b[0])
        sale_rates.append(b[1])
        purchase_rates.append(b[2])
        product_stock.append(b[3])

    return {"citcode":cit_codes,"batcode":bat_codes,"itemname":item_names,"itemunit":item_units,"purchaserate":purchase_rates,"salesrate":sale_rates,"productstock":product_stock}

# list_product() - This give the product details