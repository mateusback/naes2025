from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class ProjectCreateView(LoginRequiredMixin, CreateView):
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


class EnvironmentCreateView(LoginRequiredMixin, CreateView):
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


class FeatureFlagCreateView(LoginRequiredMixin, CreateView):
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


class RolloutRuleCreateView(LoginRequiredMixin, CreateView):
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


class ToggleLogCreateView(LoginRequiredMixin, CreateView):
    model = ToggleLog
    fields = ['feature_flag', 'user_id', 'environment', 'previous_state', 'new_state']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {
        'titulo': 'Criar Log de Alteração',
    }


class FlagSchedulerCreateView(LoginRequiredMixin, CreateView):
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
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
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


class EnvironmentUpdateView(LoginRequiredMixin, UpdateView):
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



class FeatureFlagUpdateView(LoginRequiredMixin, UpdateView):
    model = FeatureFlag
    fields = ['key', 'state', 'description', 'project']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('feature_flag_list')
    extra_context = {
        'titulo': 'Atualizar Feature Flag',
    }

    def form_valid(self, form):
        original_flag = FeatureFlag.objects.get(pk=self.object.pk)
        old_state = original_flag.state

        response = super().form_valid(form)

        new_state = form.cleaned_data['state']
        env = self.object.project.environments.first()

        print(">>> Estado original:", repr(old_state))
        print(">>> Novo estado:", repr(new_state))
        if old_state != new_state and env and self.request.user.is_authenticated:
            ToggleLog.objects.create(
                feature_flag=self.object,
                user=self.request.user,
                environment=env,
                previous_state=old_state,
                new_state=new_state,
            )
            print(">>> Log criado com sucesso.")

        return response


class ToggleLogUpdateView(LoginRequiredMixin, UpdateView):
    model = ToggleLog
    fields = ['feature_flag', 'user_id', 'environment', 'previous_state', 'new_state']
    template_name = 'form_dynamic.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {
        'titulo': 'Atualizar Log de Alteração',
    }


class RolloutRuleUpdateView(LoginRequiredMixin, UpdateView):
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


class FlagSchedulerUpdateView(LoginRequiredMixin, UpdateView):
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


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('project_list')
    extra_context = {'titulo': 'Projeto'}


class EnvironmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Environment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('environment_list')
    extra_context = {'titulo': 'Ambiente'}


class FeatureFlagDeleteView(LoginRequiredMixin, DeleteView):
    model = FeatureFlag
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('feature_flag_list')
    extra_context = {'titulo': 'Feature Flag'}


class RolloutRuleDeleteView(LoginRequiredMixin, DeleteView):
    model = RolloutRule
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('rollout_rule_list')
    extra_context = {'titulo': 'Regra de Rollout'}


class ToggleLogDeleteView(LoginRequiredMixin, DeleteView):
    model = ToggleLog
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('toggle_log_list')
    extra_context = {'titulo': 'Log de Alteração'}


class FlagSchedulerDeleteView(LoginRequiredMixin, DeleteView):
    model = FlagScheduler
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('flag_scheduler_list')
    extra_context = {'titulo': 'Agendamento de Feature Flag'}


#### List Views
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'lists/projects.html'
    context_object_name = 'projects'
    extra_context = {'titulo': 'Lista de Projetos'}

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get('q')

        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        return context


class EnvironmentListView(LoginRequiredMixin, ListView):
    model = Environment
    template_name = 'lists/environments.html'
    context_object_name = 'environments'
    extra_context = {'titulo': 'Lista de Ambientes'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('project')

        search_term = self.request.GET.get('q')
        project_id = self.request.GET.get('project')

        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['search_term'] = self.request.GET.get('q', '')
        context['selected_project'] = self.request.GET.get('project', '')
        return context

class FeatureFlagListView(LoginRequiredMixin, ListView):
    model = FeatureFlag
    template_name = 'lists/feature_flags.html'
    context_object_name = 'feature_flags' # Mudei para ser mais descritivo
    extra_context = {'titulo': 'Lista de Feature Flags'}

    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get('q')
        project_id = self.request.GET.get('project')

        if search_term:
            queryset = queryset.filter(
                Q(key__icontains=search_term) |
                Q(description__icontains=search_term)
            )

        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['search_term'] = self.request.GET.get('q', '')
        context['selected_project'] = self.request.GET.get('project', '')
        return context


class RolloutRuleListView(LoginRequiredMixin, ListView):
    model = RolloutRule
    template_name = 'lists/rollout_rules.html'
    context_object_name = 'rollout_rules'
    extra_context = {'titulo': 'Regras de Rollout'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('feature_flag')

        search_term = self.request.GET.get('q')
        flag_id = self.request.GET.get('flag')
        status = self.request.GET.get('status')
        now = timezone.now()

        if search_term:
            queryset = queryset.filter(group_name__icontains=search_term)

        if flag_id:
            queryset = queryset.filter(feature_flag_id=flag_id)

        if status == 'active':
            queryset = queryset.filter(active_from__lte=now, active_until__gte=now)
        elif status == 'scheduled':
            queryset = queryset.filter(active_from__gt=now)
        elif status == 'expired':
            queryset = queryset.filter(active_until__lt=now)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_flags'] = FeatureFlag.objects.all()
        context['search_term'] = self.request.GET.get('q', '')
        context['selected_flag'] = self.request.GET.get('flag', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class ToggleLogListView(LoginRequiredMixin, ListView):
    model = ToggleLog
    template_name = 'lists/toggle_logs.html'
    context_object_name = 'toggle_logs'
    extra_context = {'titulo': 'Histórico de Alterações'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'feature_flag', 'environment', 'user'
        ).order_by('-timestamp')

        flag_id = self.request.GET.get('flag')
        env_id = self.request.GET.get('env')
        user_id = self.request.GET.get('user')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if flag_id:
            queryset = queryset.filter(feature_flag_id=flag_id)
        if env_id:
            queryset = queryset.filter(environment_id=env_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            from datetime import datetime, timedelta
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            queryset = queryset.filter(timestamp__lt=end_date_obj)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_flags'] = FeatureFlag.objects.all()
        context['environments'] = Environment.objects.all()
        context['users'] = User.objects.all()  # Passa a lista de usuários

        # Passa os valores dos filtros atuais para o template
        context['selected_flag'] = self.request.GET.get('flag', '')
        context['selected_env'] = self.request.GET.get('env', '')
        context['selected_user'] = self.request.GET.get('user', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        return context


class FlagSchedulerListView(LoginRequiredMixin, ListView):
    model = FlagScheduler
    template_name = 'lists/flag_schedulers.html'
    context_object_name = 'schedulers'
    extra_context = {'titulo': 'Agendamentos de Flags'}

    def get_queryset(self):
        queryset = super().get_queryset().select_related('feature_flag', 'environment').order_by('scheduled_time')

        flag_id = self.request.GET.get('flag')
        env_id = self.request.GET.get('env')

        if flag_id:
            queryset = queryset.filter(feature_flag_id=flag_id)
        if env_id:
            queryset = queryset.filter(environment_id=env_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature_flags'] = FeatureFlag.objects.all()
        context['environments'] = Environment.objects.all()
        context['selected_flag'] = self.request.GET.get('flag', '')
        context['selected_env'] = self.request.GET.get('env', '')
        return context