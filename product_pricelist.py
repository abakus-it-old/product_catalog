from openerp import models, fields, api

class account_next_sequence(models.Model):
    _inherit = ['product.template']
    computed_cost_price = fields.Float(compute='_compute_cost_price',string="Cost price", store=False)
    computed_sale_price = fields.Float(compute='_compute_sale_price',string="Sale price", store=False)
    
    @api.one
    def _compute_cost_price(self):
        if self.seller_id.id:
            #-1 for error
            self.computed_cost_price = -1
            cr = self.env.cr
            uid = self.env.user.id
            obj = self.pool.get('product.supplierinfo')
            supplier_info = obj.search(cr, uid, [('product_tmpl_id', '=', self.id)])
            if supplier_info and supplier_info[0]:
                right_supplier = obj.browse(cr, uid, supplier_info[0])
                for val in obj.browse(cr, uid, supplier_info):
                    if val.sequence < right_supplier.sequence:
                        right_supplier = val
                pricelist_partnerinfo_obj = self.pool.get('pricelist.partnerinfo')
                pricelist_partnerinfos = pricelist_partnerinfo_obj.search(cr, uid, [('suppinfo_id', '=', right_supplier.id)])
                if pricelist_partnerinfos:
                    if pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).min_quantity == 0:
                        self.computed_cost_price=pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).price          
                    else:
                        self.computed_cost_price=pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).price/pricelist_partnerinfo_obj.browse(cr, uid, pricelist_partnerinfos[0]).min_quantity 
        else:
            self.computed_cost_price = self.standard_price
    
    @api.one
    def _compute_sale_price(self):
        if self.seller_id.id:
            #-1 for error
            self.computed_sale_price = -1
            cr = self.env.cr
            uid = self.env.user.id
            
            ir_property_obj = self.pool.get('ir.property')
            ir_property_id = ir_property_obj.search(cr, uid, [('name', '=', 'property_product_pricelist')])
            ir_property = ir_property_obj.browse(cr, uid, ir_property_id[0])
            
            default_pricelist_id = int(ir_property.value_reference[ir_property.value_reference.find(',')+1:]) 
            
            product_pricelist_version_obj = self.pool.get('product.pricelist.version')
            product_pricelist_version_id = product_pricelist_version_obj.search(cr, uid, [('pricelist_id', '=', default_pricelist_id),('active','=',True)])          
           
            obj = self.pool.get('product.pricelist.item')
            pricelist = obj.search(cr, uid, [('categ_id', '=', self.categ_id.id),('price_version_id','=',product_pricelist_version_id[0])])
            if pricelist:
                right_pricelist = obj.browse(cr, uid, pricelist[0])
                for val in obj.browse(cr, uid, pricelist):
                    if val.sequence < right_pricelist.sequence:
                        right_pricelist = val
                self.computed_sale_price = self.computed_cost_price*(1+right_pricelist.price_discount)+right_pricelist.price_surcharge
        else:
            self.computed_sale_price = self.list_price

