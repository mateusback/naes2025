from django.db import models
from django.contrib.auth.models import User
import uuid

class EActionType(models.TextChoices):
    ENABLE = 'ENABLE', 'Enable'
    DISABLE = 'DISABLE', 'Disable'
    TOGGLE = 'TOGGLE', 'Toggle'

    def __str__(self):
        return self.name


class EStatus(models.TextChoices):
    ENABLED = 'ENABLED', 'Enabled'
    DISABLED = 'DISABLED', 'Disabled'
    TOGGLED = 'TOGGLED', 'Toggled'

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Representa um projeto que agrupa ambientes e feature flags.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="ID do Projeto"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nome do Projeto",
        help_text="Nome único que identifica o projeto"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição geral do propósito do projeto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"


class Environment(models.Model):
    """
    Representa um ambiente de execução (ex: produção, staging, homologação).
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="ID do Ambiente"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nome do Ambiente",
        help_text="Nome que identifica o ambiente (ex: Produção, Staging)"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='environments',
        verbose_name="Projeto",
        help_text="Projeto ao qual este ambiente pertence"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Ambiente"
        verbose_name_plural = "Ambientes"


class FeatureFlag(models.Model):
    """
    Model representing a feature flag.
    """
    id = models.UUIDField(primary_key=True,
                          editable=False,
                          default=uuid.uuid4,
                          verbose_name="ID da Flag")
    key = models.CharField(max_length=255,
                           verbose_name="Chave da Flag",
                           help_text="Identificador único usado no código para referenciar a feature flag")
    state = models.CharField(max_length=10,
                             choices=EStatus.choices,
                             verbose_name="Estado",
                             help_text="Estado atual da flag: Ativada, Desativada ou Alternada")
    description = models.TextField(verbose_name="Descrição",
                                    help_text="Descrição geral da funcionalidade controlada por esta flag")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='feature_flags',
                                verbose_name="Projeto",
                                help_text="Projeto ao qual esta feature flag pertence")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name="Atualizado em")

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "Feature Flag"
        verbose_name_plural = "Feature Flags"


class RolloutRule(models.Model):
    """
    Regra de rollout controlando porcentagem de usuários que recebem a flag.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="ID da Regra"
    )
    percentage = models.PositiveSmallIntegerField(
        verbose_name="Porcentagem",
        help_text="Porcentagem de usuários que receberão a flag"
    )
    group_name = models.CharField(
        max_length=255,
        verbose_name="Nome do Grupo",
        help_text="Nome do grupo de usuários ao qual a regra se aplica"
    )
    active_from = models.DateTimeField(
        verbose_name="Ativa a partir de",
        help_text="Data e hora em que a regra começa a valer"
    )
    active_until = models.DateTimeField(
        verbose_name="Ativa até",
        help_text="Data e hora em que a regra deixa de valer"
    )
    feature_flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='rollout_rules',
        verbose_name="Feature Flag",
        help_text="Flag que está sendo controlada por esta regra"
    )

    def __str__(self):
        return f"RolloutRule {self.id} for FeatureFlag {self.feature_flag_id}"

    class Meta:
        verbose_name = "Regra de Rollout"
        verbose_name_plural = "Regras de Rollout"


class ToggleLog(models.Model):
    """
    Registro de alteração de estado de uma feature flag.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="ID do Log"
    )
    feature_flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='toggle_logs',
        verbose_name="Feature Flag",
        help_text="Flag que teve o estado alterado"
    )
    user_id = models.UUIDField(
        verbose_name="ID do Usuário",
        help_text="Usuário que realizou a alteração"
    )
    environment = models.ForeignKey(
        Environment,
        on_delete=models.CASCADE,
        related_name='toggle_logs',
        verbose_name="Ambiente",
        help_text="Ambiente no qual a alteração foi realizada"
    )
    previous_state = models.CharField(
        max_length=10,
        choices=EStatus.choices,
        verbose_name="Estado Anterior"
    )
    new_state = models.CharField(
        max_length=10,
        choices=EStatus.choices,
        verbose_name="Novo Estado"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data e Hora"
    )

    def __str__(self):
        return f"ToggleLog {self.id} for FeatureFlag {self.feature_flag.key}"

    class Meta:
        verbose_name = "Log de Alternância"
        verbose_name_plural = "Logs de Alternância"


class FlagScheduler(models.Model):
    """
    Agendamento de ação automática para uma feature flag em um ambiente.
    """
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="ID do Agendamento"
    )
    feature_flag = models.ForeignKey(
        FeatureFlag,
        on_delete=models.CASCADE,
        related_name='flag_schedulers',
        verbose_name="Feature Flag",
        help_text="Flag que será afetada pela ação"
    )
    environment = models.ForeignKey(
        Environment,
        on_delete=models.CASCADE,
        related_name='flag_schedulers',
        verbose_name="Ambiente",
        help_text="Ambiente em que a ação será aplicada"
    )
    scheduled_time = models.DateTimeField(
        verbose_name="Data Agendada",
        help_text="Momento em que a ação será executada"
    )
    action = models.CharField(
        max_length=10,
        choices=EActionType.choices,
        verbose_name="Ação",
        help_text="Tipo de ação a ser executada (Enable, Disable ou Toggle)"
    )

    def __str__(self):
        return f"FlagScheduler {self.id} for FeatureFlag {self.feature_flag.key} in Environment {self.environment.name}"

    class Meta:
        verbose_name = "Agendamento de Flag"
        verbose_name_plural = "Agendamentos de Flags"