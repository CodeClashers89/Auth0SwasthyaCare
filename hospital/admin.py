from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (CustomUser, Patient, Doctor, Appointment, MedicalRecord, 
                     DoctorAvailability, UrgentSurgery, Notification, AppointmentReschedule)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'email', 'first_name', 'last_name')}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Patient Admin"""
    list_display = ['patient_id', 'get_full_name', 'date_of_birth', 'blood_group', 'created_at']
    list_filter = ['blood_group', 'gender', 'created_at']
    search_fields = ['patient_id', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['patient_id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Doctor Admin"""
    list_display = ['get_full_name', 'specialization', 'experience_years', 'consultation_fee']
    list_filter = ['specialization']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_full_name.short_description = 'Doctor Name'


@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    """Doctor Availability Admin"""
    list_display = ['doctor', 'availability_type', 'date', 'start_time', 'end_time']
    list_filter = ['availability_type', 'date', 'doctor']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Appointment Admin"""
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'is_follow_up']
    list_filter = ['status', 'is_follow_up', 'appointment_date', 'doctor']
    search_fields = ['patient__patient_id', 'patient__user__first_name', 'doctor__user__first_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    """Medical Record Admin"""
    list_display = ['patient', 'doctor', 'appointment', 'created_at']
    list_filter = ['created_at', 'doctor']
    search_fields = ['patient__patient_id', 'patient__user__first_name', 'diagnosis']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UrgentSurgery)
class UrgentSurgeryAdmin(admin.ModelAdmin):
    """Urgent Surgery Admin"""
    list_display = ['surgery_type', 'doctor', 'patient_name', 'surgery_date', 'start_time', 'end_time', 'status', 'created_by']
    list_filter = ['status', 'surgery_date', 'created_at']
    search_fields = ['surgery_type', 'patient_name', 'doctor__user__first_name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification Admin"""
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']


@admin.register(AppointmentReschedule)
class AppointmentRescheduleAdmin(admin.ModelAdmin):
    """Appointment Reschedule Admin"""
    list_display = ['appointment', 'original_date', 'original_time', 'new_date', 'new_time', 'rescheduled_by', 'created_at']
    list_filter = ['created_at', 'original_date', 'new_date']
    search_fields = ['appointment__patient__patient_id', 'reason']

