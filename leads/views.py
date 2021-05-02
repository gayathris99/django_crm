from django.shortcuts import render , redirect , reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm , LeadModelForm , CustomUserCreationForm
from django.views.generic import TemplateView , DeleteView ,UpdateView , ListView , DetailView , CreateView
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserAndLoginRequiredMixin

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render(request, 'landing.html')


 

class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation = user.userprofile ,
                agent__isnull =  False
                ) 
        else:
            queryset = Lead.objects.filter(
                organisation = user.agent.organisation, 
                agent__isnull = False
                )
            queryset = queryset.filter(agent__user = user)
            #filter the agent based on the user it is asscoiated with
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView,self).get_context_data(**kwargs)
        if user.is_organiser:
            queryset = Lead.objects.filter(
                organisation =  user.userprofile,
             agent__isnull = True
             )
            context.update({
                "unassigned_leads": queryset
            }
            )
        return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request, 'leads/lead_list.html',context)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'leads/lead_detail.html' 
    queryset = Lead.objects.all()
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation = user.userprofile) 
        else:
            queryset = Lead.objects.filter(organisation = user.agent.organisation)
            queryset = queryset.filter(agent__user = user)
            #filter the agent based on the user it is asscoiated with
        return queryset

    
def lead_detail(request , pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead":lead
    }
    return render(request , 'leads/lead_detail.html' , context)


class LeadCreateView(OrganiserAndLoginRequiredMixin,CreateView):
    template_name = 'leads/lead_create.html'
    form_class = LeadModelForm

    

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        #sending emails
        send_mail(
            subject = "Lead has been created",
            message= "Go to the site to see the new lead",
            from_email= "gayathri.s@campusuvce.in",
            recipient_list = ["gayathri11499@gmail.com" ,]
        )
        return super(LeadCreateView,self).form_valid(form)


def lead_create(request):
    #Lead form is the form which doesnt use the already built in model, 
    # and hence we  areusing lead.objects.create to save the
    #form details into the model

    # form = LeadForm()
    # if request.method == "POST":
        # print("post request")
        # form = LeadForm(request.POST)
        # if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = Agent.objects.first()
            # Lead.objects.create(
                # first_name= first_name,
                # last_name=last_name,
                # age = age,
                # agent = agent
            # )
            # return redirect("/leads")
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")

    context = {
        "form":form

    }
    return render(request, 'leads/lead_create.html', context)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'leads/lead_update.html'
    
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance = lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance = lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, 'leads/lead_update.html',context)

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organisation=user.userprofile)


    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request,pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect("/leads")

# def lead_update(request ,pk):
    # lead = Lead.objects.get(id=pk)
    # form = LeadForm()
    # if request.method == "POST":
        # print("post request")
        # form = LeadForm(request.POST)
        # if form.is_valid():
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # 
            # lead.first_name = first_name
            # lead.last_name = last_name
            # lead.age = age
# 
            # lead.save()
            # return redirect("/leads")
    # context = {
        # "lead" :lead,
        # "form":form
    # }
    # return render(request, 'leads/lead_update.html',context)
