from django.contrib import admin

# Register your models here.
from contract_app.models import Contract, PayInfo
from utils.CrmAdmin import CrmAdmin


class PayInfoAdmin(admin.StackedInline):
    model = PayInfo
    extra = 1


@admin.register(Contract)
class ContractAdmin(CrmAdmin, admin.ModelAdmin):
    inlines = (PayInfoAdmin,)
    list_display = ('code', 'name', 'project_id', 'is_inner_contract')
    list_filter = ('is_accepted', 'code', 'name', 'project_id')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False

    def has_add_permission(self, request):
        return True

    # is_inner_contract 是一个纯用来展示的，不可更改的字段。它不存在model中，但又有展示的需求
    @admin.display(boolean=True, description='是否内部合同')
    def is_inner_contract(self, obj):
        return obj.code.startswith('000')
