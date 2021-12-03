from django.shortcuts import render

from .forms import ImageForm


def home_view(request):
    template = "plug.html"
    content = ""
    context = {"content": content}

    return render(request, template, context)


def image_upload_view(request):
    """Process images uploaded by users"""
    template = "plug.html"
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, template, {"form": form, "img_obj": img_obj})
    else:
        form = ImageForm()
    return render(request, template, {"form": form})
