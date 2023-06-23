from django.contrib import admin

from crypto.models import Asset, Order, PostponedOrder, Suitcase, Wallet

admin.site.register(Asset)
admin.site.register(Order)
admin.site.register(PostponedOrder)
admin.site.register(Suitcase)
admin.site.register(Wallet)
