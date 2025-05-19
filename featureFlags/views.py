from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import *

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'description']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('project_list')
    extra_context = {
        'titulo': 'Criar Projeto',
    }

    def form_valid(self, form):
        messages.success(self.request, "Projeto salvo com sucesso!")
        return super().form_valid(form)


class EnvironmentCreateView(CreateView):
    model = Environment
    fields = ['name', 'project']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('environment_list')
    extra_context = {
        'titulo': 'Criar Ambiente',
    }

    def form_valid(self, form):
        messages.success(self.request, "Ambiênte salvo com sucesso!")
        return super().form_valid(form)


class FeatureFlagCreateView(CreateView):
    model = FeatureFlag
    fields = ['key', 'state', 'description', 'project']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('feature_flag_list')
    extra_context = {
        'titulo': 'Criar Feature Flag',
    }

    def form_valid(self, form):
        messages.success(self.request, "Feature Flag salva com sucesso!")
        return super().form_valid(form)


class RolloutRuleCreateView(CreateView):
    model = RolloutRule
    fields = ['percentage', 'group_name', 'active_from', 'active_until', 'feature_flag']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('rollout_rule_list')
    extra_context = {
        'titulo': 'Criar Regra de Rollout',
    }

    def form_valid(self, form):
        messages.success(self.request, "Regra salva com sucesso!")
        return super().form_valid(form)


class ToggleLogCreateView(CreateView):
    model = ToggleLog
    fields = ['feature_flag', 'user_id', 'environment', 'previous_state', 'new_state']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {
        'titulo': 'Criar Log de Alteração',
    }


class FlagSchedulerCreateView(CreateView):
    model = FlagScheduler
    fields = ['feature_flag', 'environment', 'scheduled_time', 'action']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('flag_scheduler_list')
    extra_context = {
        'titulo': 'Criar Agendamento de Feature Flag',
    }

    def form_valid(self, form):
        messages.success(self.request, "Agendamento salvo com sucesso!")
        return super().form_valid(form)


#### Update Views
class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'description']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('project_list')
    extra_context = {
        'titulo': 'Atualizar Projeto',
    }

    def form_valid(self, form):
        messages.success(self.request, "Projeto Salvo com sucesso!")
        return super().form_valid(form)


class EnvironmentUpdateView(UpdateView):
    model = Environment
    fields = ['name', 'project']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('environment_list')
    extra_context = {
        'titulo': 'Atualizar Ambiente',
    }

    def form_valid(self, form):
        messages.success(self.request, "Ambiênte salvo com sucesso!")
        return super().form_valid(form)


class FeatureFlagUpdateView(UpdateView):
    model = FeatureFlag
    fields = ['key', 'state', 'description', 'project']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('feature_flag_list')
    extra_context = {
        'titulo': 'Atualizar Feature Flag',
    }
    def form_valid(self, form):
        messages.success(self.request, "Feature Flag salva com sucesso!")
        return super().form_valid(form)


class ToggleLogUpdateView(UpdateView):
    model = ToggleLog
    fields = ['feature_flag', 'user_id', 'environment', 'previous_state', 'new_state']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {
        'titulo': 'Atualizar Log de Alteração',
    }


class RolloutRuleUpdateView(UpdateView):
    model = RolloutRule
    fields = ['percentage', 'group_name', 'active_from', 'active_until', 'feature_flag']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('rollout_rule_list')
    extra_context = {
        'titulo': 'Atualizar Regra de Rollout',
    }

    def form_valid(self, form):
        messages.success(self.request, "Regra salva com sucesso!")
        return super().form_valid(form)


class FlagSchedulerUpdateView(UpdateView):
    model = FlagScheduler
    fields = ['feature_flag', 'environment', 'scheduled_time', 'action']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('flag_scheduler_create')
    extra_context = {
        'titulo': 'Atualizar Agendamento de Feature Flag',
    }

    def form_valid(self, form):
        messages.success(self.request, "Feature Flag salva com sucesso!")
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('project_list')
    extra_context = {'titulo': 'Projeto'}


class EnvironmentDeleteView(DeleteView):
    model = Environment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('environment_list')
    extra_context = {'titulo': 'Ambiente'}


class FeatureFlagDeleteView(DeleteView):
    model = FeatureFlag
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('feature_flag_list')
    extra_context = {'titulo': 'Feature Flag'}


class RolloutRuleDeleteView(DeleteView):
    model = RolloutRule
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('rollout_rule_list')
    extra_context = {'titulo': 'Regra de Rollout'}


class ToggleLogDeleteView(DeleteView):
    model = ToggleLog
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {'titulo': 'Log de Alteração'}


class FlagSchedulerDeleteView(DeleteView):
    model = FlagScheduler
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('flag_scheduler_list')
    extra_context = {'titulo': 'Agendamento de Feature Flag'}


#### List Views
class ProjectListView(ListView):
    model = Project
    template_name = 'lists/projects.html'
    context_object_name = 'projects'
    extra_context = {
        'titulo': 'Lista de Projetos',
    }

class EnvironmentListView(ListView):
    model = Environment
    template_name = 'lists/environments.html'
    context_object_name = 'environments'
    extra_context = {'titulo': 'Lista de Ambientes'}


class FeatureFlagListView(ListView):
    model = FeatureFlag
    template_name = 'lists/feature_flags.html'
    context_object_name = 'feature_flags'
    extra_context = {'titulo': 'Lista de Feature Flags'}


class RolloutRuleListView(ListView):
    model = RolloutRule
    template_name = 'lists/rollout_rules.html'
    context_object_name = 'rollout_rules'
    extra_context = {'titulo': 'Lista de Regras de Rollout'}


class ToggleLogListView(ListView):
    model = ToggleLog
    template_name = 'lists/toggle_logs.html'
    context_object_name = 'toggle_logs'
    extra_context = {'titulo': 'Histórico de Alterações'}


class FlagSchedulerListView(ListView):
    model = FlagScheduler
    template_name = 'lists/flag_schedulers.html'
    context_object_name = 'flag_schedulers'
    extra_context = {'titulo': 'Agendamentos de Flags'}