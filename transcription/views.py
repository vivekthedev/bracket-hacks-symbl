from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from .video_transcription import get_transcription
from .models import Video
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django import forms
import json


class HomePage(TemplateView):
    template_name = "index.html"


def video_page(request):
    text_form = {}
    messages = []
    if request.method == "POST":
        video = request.FILES.get("video")
        filename = video.name
        path = video.temporary_file_path()
        messages = get_transcription(path)
        text_form = [
            f'{x["start_timestamp"]} - {x["end_timestamp"]} : {x["text"]}'
            for x in messages
        ]
        if request.user.is_authenticated:
            Video.objects.create(done_by=request.user, transcript=messages)
        text_form = "\n\n".join(text_form)

    return render(
        request, "results.html", context={"messages": text_form, "json": messages}
    )


def history(request):
    documents = {}
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        documents = Video.objects.filter(done_by=user)
    return render(request, "history.html", {"documents": documents})


def document(request, doc_id):
    document = Video.objects.get(id=doc_id)
    json_text = json.dumps(document.transcript, indent=2)
    text_form = []

    return render(
        request, "single.html", context={"messages": text_form, "json": json_text}
    )


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    fields = ["username", "email", "password"]
    model = User

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return redirect("/")

    def get_form(self):
        form = super(SignUpView, self).get_form()
        form.fields["password"].widget = forms.PasswordInput()
        return form
