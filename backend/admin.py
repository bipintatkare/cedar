from django.contrib import admin

from backend.models import adminModel, costCategoryModel, costExpenseModel, costModel, expenseTypeModel,  otpModel, reservationModel, sessionModel, settingsModel

# Register your models here.


class sessionAdmin(admin.ModelAdmin):
    list_display = (['email'])


class otpAdmin(admin.ModelAdmin):
    list_display = (['email'])


class adminsAdmin(admin.ModelAdmin):
    list_display = (['name'])


class settingsAdmin(admin.ModelAdmin):
    list_display = (['url'])


class reservationAdmin(admin.ModelAdmin):
    list_display = (['reservationNo'])


class costCategoryAdmin(admin.ModelAdmin):
    list_display = (['category'])


class expenseTypeAdmin(admin.ModelAdmin):
    list_display = (['typ'])


class costAdmin(admin.ModelAdmin):
    list_display = (['amount'])


class costExpenseAdmin(admin.ModelAdmin):
    list_display = (['amount'])


admin.site.register(costExpenseModel, costExpenseAdmin)
admin.site.register(costModel, costAdmin)
admin.site.register(expenseTypeModel, expenseTypeAdmin)
admin.site.register(costCategoryModel, costCategoryAdmin)
admin.site.register(reservationModel, reservationAdmin)
admin.site.register(settingsModel, settingsAdmin)
admin.site.register(adminModel, adminsAdmin)
admin.site.register(otpModel, otpAdmin)
admin.site.register(sessionModel, sessionAdmin)
