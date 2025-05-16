from django.urls import path
from .views import *

urlpatterns = [
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('environments/create/', EnvironmentCreateView.as_view(), name='environment_create'),
    path('feature-flags/create/', FeatureFlagCreateView.as_view(), name='feature_flag_create'),
    path('rollout-rules/create/', RolloutRuleCreateView.as_view(), name='rollout_rule_create'),
    path('toggle-logs/create/', ToggleLogCreateView.as_view(), name='toggle_log_create'),
    path('flag-schedulers/create/', FlagSchedulerCreateView.as_view(), name='flag_scheduler_create'),

    path('projects/edit/<pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('environments/edit/<pk>/', EnvironmentUpdateView.as_view(), name='environment_update'),
    path('feature-flags/edit/<pk>/', FeatureFlagUpdateView.as_view(), name='feature_flag_update'),
    path('rollout-rules/edit/<pk>/', RolloutRuleUpdateView.as_view(), name='rollout_rule_update'),
    path('toggle-logs/edit/<pk>/', ToggleLogUpdateView.as_view(), name='toggle_log_update'),
    path('flag-schedulers/edit/<pk>/', FlagSchedulerUpdateView.as_view(), name='flag_scheduler_update'),

    path('projects/delete/<pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('environments/delete/<pk>/', EnvironmentDeleteView.as_view(), name='environment_delete'),
    path('feature-flags/delete/<pk>/', FeatureFlagDeleteView.as_view(), name='feature_flag_delete'),
    path('rollout-rules/delete/<pk>/', RolloutRuleDeleteView.as_view(), name='rollout_rule_delete'),
    path('toggle-logs/delete/<pk>/', ToggleLogDeleteView.as_view(), name='toggle_log_delete'),
    path('flag-schedulers/delete/<pk>/', FlagSchedulerDeleteView.as_view(), name='flag_scheduler_delete'),

    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('environments/', EnvironmentListView.as_view(), name='environment_list'),
    path('feature-flags/', FeatureFlagListView.as_view(), name='feature_flag_list'),
    path('rollout-rules/', RolloutRuleListView.as_view(), name='rollout_rule_list'),
    path('toggle-logs/', ToggleLogListView.as_view(), name='toggle_log_list'),
    path('flag-schedulers/', FlagSchedulerListView.as_view(), name='flag_scheduler_list'),
]
