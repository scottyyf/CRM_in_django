from django.contrib import admin

# Register your models here.
from project_app.models import Projects, Processes
from utils.CrmAdmin import CrmAdmin


# 将两个表 或多个表 放在同一个admin去处理， 用Inline
class ProcessesInline(admin.StackedInline):
    model = Processes
    # 每次出现几个对象在另外的对象中
    extra = 1


@admin.register(Projects)
class ProjectAdmin(CrmAdmin, admin.ModelAdmin):
    # inline的对象出现在该对象中，用户可以查看
    inlines = [ProcessesInline,]

    list_display = ('name', 'project_id')
    fields = ('name', 'project_id', 'budget', 'get_percent', 'customer',
              'tel', 'salesman', 'sales_department')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        qs = qs.filter(salesman=request.user.id)
        return qs

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()

        # 新增一个项目时，obj为空
        if not obj:
            return ()

        return ('budget', 'get_percent', 'project_id')

    def has_add_permission(self, request):
        return True




