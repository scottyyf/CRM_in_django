from django.contrib import admin

# Register your models here.
from user_app.models import User, Role, Department
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as UA
from Index import index_decorator, find_model_index
from utils.CrmAdmin import CrmAdmin


@admin.register(User)
class UserAdmin(UA):
    # @admin.display(empty_value='--empty--')
    # def view_tel_num(self, obj):
    #     return obj.tel
    # 首页界面空值 展示
    empty_value_display = '--empty--'
    # fields = ('username', 'email', 'tel', 'department', 'job', 'password')
    # 首页上将action按钮放在下方
    actions_on_bottom = True
    actions_on_top = False

    # 清除首页所有action动作选项
    actions = None

    # 定义每条项目保存时的动作.
    # def save_model(self, request, obj, form, change):
    #     obj.is_staff = True
    #     obj.save()

    # 是否有增加新条目的权限
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        return False

    # 定义首尔上的排序,返回值要和后面的ordering类似
    def get_ordering(self, request):
        ordering = ('-department__groups',)
        return ordering

    # 首页进入后，展示的东西也可以定制
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            # 下面这 在新增用户时只有username passwd1 passwd2这三个字段，且只有一个元素
            ori = super().get_fieldsets(request, obj)
            # 新增动作时，obj为None
            if obj:
                ori[1][1].update(self.sfieldsets[1][1])

            # 设置可修改的首页字段
            self.list_editable = ('job',)
            return ori

        self.list_editable = ()
        return self.sfieldsets

    # 进入后 展示的项目 关键字是fieldsets, 下面这个是为了区分这个关键字，所以加了s
    sfieldsets = (
        # 用户登录，需要用到is_staff,否则无法登录，这里建议用UserAdmin里面的内容进行展示
        (None, {
            'fields': ('username', ),
            # 'description': '姓名'
            }),
        ('Advanced options', {
            'fields': ('email', 'tel', 'is_staff', 'department', 'job', 'password'),
            'classes': ('collapse',),
            # 'description': '属性'
            })
    )

    # 首页显示的内容定制，查询显示的内容顾虑，不显示所有的
    def get_queryset(self, request):
        user_id = request.user.id
        # userprofile = User.objects.all()

        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        ret = qs.filter(id=user_id)
        return ret

    # 进入首页后，针对不同的人设置不同的readonly
    def get_readonly_fields(self, request, obj=None):
        """superuser 没有readonly，其他人有"""
        if request.user.is_superuser:
            self.readonly_fields = ()
        return self.readonly_fields

    # 首页上展示时，自定义展示的字段
    @admin.display(description='用户：部门')
    def list_user_dpt(self):
        return f'{self.username}： {self.department}'

    # 首页展示的字段
    list_display = (list_user_dpt, 'job')
    # 首页链接放置的字段
    list_display_links = (list_user_dpt,)
    # 首页字段可改的字段, 因为要设置不同用户的editable的东西，这里就注销
    # list_editable = ('job',)
    # 首页过滤的字段， 可通过__选择外键的字段
    list_filter = ('username', 'department__groups', 'job', 'tel')
    # 首页展示的数目
    list_max_show_all = 10
    list_per_page = 10
    # 首页展示的排序
    ordering = ('department__groups',)
    # 首页进入后，choice选项的展示，是垂直还是并排，如果展示的字段在这个字典中就会进行应用
    radio_fields = {'department': admin.HORIZONTAL, 'job': admin.HORIZONTAL}
    # 首页进入后的只读字段
    readonly_fields = ('username', 'job', 'department', 'is_staff', )
    # 修改完成后，继续到该修改的视图
    save_as_continue = True
    # 首页上，出现搜索的窗口, 对于外键 需要定义到具体字段
    search_fields = ('username', 'tel', 'department__name', 'job__name')
    # 首页上，进行过滤时，是否显示过滤的总结果，默认开启可能在大量数据下降低性能
    show_full_result_count = False


@admin.register(Role)
class RoleAdmin(CrmAdmin, admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        user = User.objects.get(username=request.user)
        job = user.job
        ret = qs.filter(name=job)
        return ret

    def get_ordering(self, request):
        return ('name', )

    # 首页list_display的动态，用户字段展示
    def get_list_display(self, request):
        if request.user.is_superuser:
            list_display = ('name', 'create_time', 'update_time')
        else:
            list_display = ('name', 'create_time')
        return list_display

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = ()
        else:
            readonly_fields = ('name',)
        return readonly_fields

    # 定义首页搜索的字段
    def get_search_fields(self, request):
        return ('name', 'user__username', 'create_time')

    def get_list_filter(self, request):
        return ('name', 'create_time')


@admin.register(Department)
class DepartmentAdmin(CrmAdmin, admin.ModelAdmin):

    list_display = ('name', 'groups', 'parent')
    # list_editable = ('groups', 'parent')

    fieldsets = (
        ('属性', {'fields': ('name', 'parent', 'groups')}),
        )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            self.list_editable = ('groups', 'parent')
            readonly_fd = ()
        else:
            readonly_fd = ('name', 'parent', 'groups')
            self.list_editable = ()

        return readonly_fd


# admin.site.register(User)
admin.site.site_header = '万里公司销售系统'
admin.site.site_title = '万里行'
admin.site.index_title = '销售系统管理'

# 展示的顺序
admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

# 大屏时是否有左侧导航，默认true
admin.site.enable_nav_sidebar = True

# admin.site.register(Role)
# admin.site.register(Department)