from openerp import models, fields, api

class product_template_pricelist(models.Model):
    _inherit = ['product.template']
    computed_sale_price = fields.Float(compute='_compute_sale_price', string="Computed sale price")
    suppliers_list = fields.Char(compute='_computeSuppliersList', string="Suppliers")

    @api.one
    @api.depends('seller_ids')
    def _computeSuppliersList(self):
        if len(self.seller_ids) > 0:
            text = str(len(self.seller_ids)) + " ("
            for seller in self.seller_ids:
                text += seller.name.name + ', '
            text += ")"
            self.suppliers_list = text

    @api.one
    def _compute_sale_price(self):
        if len(self.seller_ids) > 0:
            #-1 for error
            self.computed_sale_price = -1
            cr = self.env.cr
            uid = self.env.user.id
            
            ir_property_obj = self.pool.get('ir.property')
            ir_property_id = ir_property_obj.search(cr, uid, [('name', '=', 'property_product_pricelist')])
            ir_property = ir_property_obj.browse(cr, uid, ir_property_id[0])
            
            default_pricelist_id = int(ir_property.value_reference[ir_property.value_reference.find(',')+1:]) 
            
            obj = self.pool.get('product.pricelist.item')
            pricelist = obj.search(cr, uid, [('categ_id', '=', self.categ_id.id),('pricelist_id','=',default_pricelist_id)])
            if pricelist:
                right_pricelist = obj.browse(cr, uid, pricelist[0])
                for val in obj.browse(cr, uid, pricelist):
                    if val.sequence < right_pricelist.sequence:
                        right_pricelist = val
                
                margin = (right_pricelist.price_discount / 100) * -1 # cause it is stored like: 20% margin => '-20%"
                price = self.standard_price * (1 + margin)
                price = price + right_pricelist.price_surcharge
                self.computed_sale_price = price
        else:
            self.computed_sale_price = self.lst_price

class product_product_pricelist(models.Model):
    _inherit = ['product.product']
    computed_sale_price = fields.Float(related="product_tmpl_id.computed_sale_price", string="Computed sale price")
    
    
