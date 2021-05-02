from django.shortcuts import render, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent , UserProfile
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
import random


class AgentListView(OrganiserAndLoginRequiredMixin , generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        # return Agent.objects.all()
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganiserAndLoginRequiredMixin , generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit = False)
        user.is_agent = True
        user.is_organiser = False
        user.save()
        user.set_password(f"{random.randint(0,100000)}")
        Agent.objects.create(
            user = user,
            organisation= self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent",
            message = "You are agent application has been accepted, Please come login to work",
            from_email = "admin@test.com",
            receipient_list = [user.email]
        )
        # agent.organisation = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)


class AgentDetailView(OrganiserAndLoginRequiredMixin , generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganiserAndLoginRequiredMixin , generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(OrganiserAndLoginRequiredMixin , generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        # return Agent.objects.all()
        return Agent.objects.filter(organisation=organisation)



    def get_success_url(self):
        return reverse("agents:agent-list")