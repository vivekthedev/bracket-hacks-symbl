from django.shortcuts import render
from django.views.generic import TemplateView
from .video_transcription import get_transcription


class HomePage(TemplateView):
    template_name = "index.html"


def video_page(request):
    text_form = {"jhajs": "dfa"}
    messages = [{"jhajs": "dfa"}, {"jhajs": "dfas"}]
    if request.method == "POST":
        video = request.FILES.get("video")
        filename = video.name
        path = video.temporary_file_path()
        messages = get_transcription(path)
        text_form = [
            f'{x["start_timestamp"]} - {x["end_timestamp"]} : {x["text"]}'
            for x in messages
        ]
        text_form = "\n\n".join(text_form)

    return render(
        request, "results.html", context={"messages": text_form, "json": messages}
    )
