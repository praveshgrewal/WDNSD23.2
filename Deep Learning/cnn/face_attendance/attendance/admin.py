from django.contrib import admin
from .models import Employee, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'email', 'department', 'is_trained', 'images_count', 'created_at']
    list_filter = ['is_trained', 'department']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'images_count']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out', 'status', 'confidence', 'duration']
    list_filter = ['status', 'date']
    search_fields = ['employee__name']
    date_hierarchy = 'date'

    def duration(self, obj):
        return obj.duration
    duration.short_description = 'Duration'
