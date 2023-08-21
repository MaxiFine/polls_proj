import random
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView,TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Polls, OneTimeCode
from .forms import PollsQuestionForm, SharePollForm, EditPollForm


# HomePage
class HomePageView(TemplateView):
    template_name = 'home.html'

# About Page
class AboutPageView(TemplateView):
    template_name = 'about.html'

# Listing Polls by User
class PollsListView(ListView):
    template_name = 'polls/list_polls.html'
    paginate_by = 3 
    context_object_name = 'poll'

    def get_queryset(self):
        querryset = Polls.objects.all()
        querryset = querryset.order_by('-id')
        return querryset

    
# Creating a Poll
class PollsCreateView(CreateView):
    form_class = PollsQuestionForm
    template_name = 'polls/create_polls.html'
    success_url = reverse_lazy('list_polls')

    def form_valid(self, form):
        # Generate a new 6-digit code
        code = random.randint(100000, 999999)

        # Store the code in the OneTimeCode model
        email = form.cleaned_data.get('pc_mail')
        if email:
            # Check if a OneTimeCode object already exists for this email and poll
            try:
                existing_code = OneTimeCode.objects.get(email=email, poll=None)
                existing_code.delete()
            except OneTimeCode.DoesNotExist:
                pass

            # Create a new OneTimeCode
            code = OneTimeCode.objects.create(email=email, code=code)
            
            # Send the code to the user's email
            subject = "Your One-Time Code for Poll Creation"
            message = f"Your one-time code for poll creation: {code}"
            send_mail(subject, message, 'your_email@example.com', [email])

        # Proceed with poll creation
        return super().form_valid(form)




# Post Details
class PollDetailView(DetailView):
    model = Polls
    template_name = 'polls/polls_detail.html'


def share_poll(request, pk):
    # Retrieve poll by id
    poll = get_object_or_404(Polls, pk=pk,)
    sent = False

    if request.method == 'POST':
        form = SharePollForm(request.POST)
        if form.is_valid():

            # Form fields passed validation
            cd = form.cleaned_data
            # ... send the mail
            post_url = request.build_absolute_uri(poll.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{poll.question}"
            message = f"Read {poll.question} at {post_url}\n\n" f"{cd['name']}"
            send_mail(subject, message, 'sikapa75@gmail.com', [cd['to']])
            sent = True            

            messages.success(request, 'Your Poll have been Sent')
            return redirect('poll_detail', pk=pk)
    else:
        form = SharePollForm()
    return render(request, 'polls/share_poll.html', 
                  {'poll': poll, 
                   'form': form,
                   'sent': sent,})


class EditPollView(UpdateView):
    model = Polls
    form_class = EditPollForm
    template_name = 'polls/edit_poll.html'
    context_object_name = 'poll'

    def form_valid(self, form):
        edit_poll = form.save(commit=False)
        edit_poll.save()
        return redirect('poll_detail', pk=edit_poll.pk)


def vote(request, pk):
    poll = Polls.objects.get(pk=pk)
    if request.method == "POST":
        choice = request.POST.get('option','')
        if choice == poll.option1:
            poll.option1_count += 1
        elif choice == poll.option2:
            poll.option2_count += 1
        elif choice == poll.option3:
            poll.option3_count += 1
        else:
            messages.warning(request, "Sorry You cannot Vote today\n Invalid Form")
        
        poll.save()
        return redirect('poll_results', poll.pk)
    else:     
        context = {'poll': poll,}
    return render(request, 'polls/votes.html', context)


def results(request, poll_id):
    poll_question = Polls.objects.get(id=poll_id)
    context = {
        'poll': poll_question,
    }
    return render(request, 'polls/results.html', context)


