from django.contrib import admin

from .models import (
    Organization, Domain, OrganizationUser,
    TrainingCourse, Certification,
    StrategicPlan, StrategicAxis,
    PlanAction, PlanActionMember, Effet, Produit, Action, Activite, ActiviteLog,
)


class DomainInline(admin.TabularInline):
    model = Domain
    extra = 1


class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    extra = 1
    raw_id_fields = ['user']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active']
    search_fields = ['name', 'slug']
    inlines = [DomainInline, OrganizationUserInline]


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'organization', 'is_primary', 'is_active']
    list_filter = ['is_primary', 'is_active']
    search_fields = ['domain', 'organization__name']
    autocomplete_fields = ['organization']


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_admin', 'joined_at']
    list_filter = ['role', 'is_admin', 'organization']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'organization__name']
    autocomplete_fields = ['user', 'organization']


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'duration_hours', 'is_active']
    list_filter = ['is_active', 'organization']
    search_fields = ['title', 'organization__name']


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'organization', 'level']
    list_filter = ['level', 'organization']
    search_fields = ['name', 'course__title']


@admin.register(StrategicPlan)
class StrategicPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'start_year', 'horizon', 'is_active']
    list_filter = ['is_active', 'organization']
    search_fields = ['title', 'organization__name']


@admin.register(StrategicAxis)
class StrategicAxisAdmin(admin.ModelAdmin):
    list_display = ['name', 'axis_type', 'plan', 'organization', 'weight']
    list_filter = ['axis_type', 'organization']
    search_fields = ['name', 'plan__title']


class PlanActionMemberInline(admin.TabularInline):
    model = PlanActionMember
    extra = 1
    raw_id_fields = ['user']


@admin.register(PlanAction)
class PlanActionAdmin(admin.ModelAdmin):
    list_display = ['reference', 'titre', 'organization', 'annee_debut', 'horizon']
    list_filter = ['organization', 'annee_debut']
    search_fields = ['titre', 'reference']
    inlines = [PlanActionMemberInline]


@admin.register(PlanActionMember)
class PlanActionMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan_action', 'role', 'invited_at']
    list_filter = ['role', 'plan_action']
    search_fields = ['user__email', 'user__first_name', 'plan_action__titre']


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['reference', 'titre', 'organization', 'action']
    list_filter = ['organization']
    search_fields = ['titre', 'reference']
