from django.contrib import admin
from core.views import *

admin.site.register(add_product)
admin.site.register(product_list)
admin.site.register(create_category)
admin.site.register(category_list)
admin.site.register(blog_detail)
admin.site.register(blog_list)
admin.site.register(book_list)
admin.site.register(book_detail)
admin.site.register(create_or_update_account)
admin.site.register(customer_form)
admin.site.register(create_shipment)
admin.site.register(delete_shipment)
admin.site.register(shipment_list)
admin.site.register(shipment_detail)