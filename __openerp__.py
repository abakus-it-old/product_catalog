{
    'name': "Products catalog with prices",
    'version': '9.0.1.1',
    'depends': ['sale', 'product', 'product_cost_price_from_suppliers'],
    'author': "Valentin THIRION & Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sale',
    'description': """
    Product Catalog
    
This module adds a list of products in the sale application with the computed sale price regarding pricelists, supplier prices etc.

It also adds a field in the product views with the computed sale price regarding the default pricelists.
It also colors the lines in order to improve visibility.

This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': ['product_pricelist.xml',],
}
