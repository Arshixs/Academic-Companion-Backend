from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

User = get_user_model()

class CodeSnippet(models.Model):
    """Model to store code snippets"""
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('cpp', 'C++'),
        ('c', 'C'),
        ('javascript', 'JavaScript'),
    ]
    
    title = models.CharField(
        max_length=255,
        help_text=_("Title of the code snippet")
    )
    description = models.TextField(
        blank=True,
        help_text=_("Description of what the code does")
    )
    code = models.TextField(
        validators=[MaxLengthValidator(50000)],
        help_text=_("The actual code content")
    )
    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        help_text=_("Programming language of the code")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='code_snippets',
        help_text=_("User who created this snippet")
    )
    is_public = models.BooleanField(
        default=False,
        help_text=_("Whether this snippet is publicly visible")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'language']),
            models.Index(fields=['is_public', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.title} ({self.language})"

class ExecutionHistory(models.Model):
    """Model to track code execution history"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
    ]
    
    snippet = models.ForeignKey(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name='executions',
        null=True,
        blank=True,
        help_text=_("Related code snippet if saved")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='code_executions',
        help_text=_("User who executed the code")
    )
    code = models.TextField(
        help_text=_("Code that was executed")
    )
    language = models.CharField(
        max_length=20,
        choices=CodeSnippet.LANGUAGE_CHOICES,
        help_text=_("Programming language used")
    )
    output = models.TextField(
        blank=True,
        help_text=_("Output of code execution")
    )
    error = models.TextField(
        blank=True,
        help_text=_("Error message if execution failed")
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        help_text=_("Status of code execution")
    )
    execution_time = models.FloatField(
        help_text=_("Time taken to execute (seconds)")
    )
    memory_usage = models.IntegerField(
        null=True,
        blank=True,
        help_text=_("Memory used during execution (KB)")
    )
    executed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-executed_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['executed_at']),
        ]
        
    def __str__(self):
        return f"{self.user.username}'s {self.language} execution at {self.executed_at}"

class CodeTemplate(models.Model):
    """Model for predefined code templates"""
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(
        max_length=20,
        choices=CodeSnippet.LANGUAGE_CHOICES
    )
    template_code = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['language', 'title']
        
    def __str__(self):
        return f"{self.title} ({self.language})"