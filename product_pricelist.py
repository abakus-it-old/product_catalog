from openerp import models, fields, api

class product_product_pricelist(models.Model):
    _inherit = ['product.product']
    computed_cost_price = fields.Float(compute='_compute_cost_price',string="Cost price", store=False)
    computed_sale_price = fields.Float(compute='_compute_sale_price',string="Sale price", store=False)
    
    @api.one
    def _compute_cost_price(self):
		cr = self.env.cr
		uid = self.env.user.id

    	# Product as sellers
		if len(self.seller_ids) > 0:
			# get supplier info
			obj = self.pool.get('product.supplierinfo')
			supplier_info_ids = obj.search(cr, uid, [('product_tmpl_id', '=', self.product_tmpl_id.id)], order='sequence ASC')
			if len(supplier_info_ids) > 0:
				right_supplier = obj.browse(cr, uid, supplier_info_ids[0])
				self.computed_cost_price = right_supplier.price
		else:
			self.computed_cost_price = self.standard_price
    
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
                self.computed_sale_price = self.computed_cost_price*(1+right_pricelist.price_discount)+right_pricelist.price_surcharge
        else:
            self.computed_sale_price = self.lst_price
