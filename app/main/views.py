from django.shortcuts import render
from .forms import ImageFaceForm
from .forms import ImageRubbishForm
from django.http import HttpResponseRedirect
from .neuralnetworkrubbish import nnrubbish
from .neuralnetworkface import nnface


def ImageFace_upload_view(request):
    template = 'cam.html'
    if request.method == 'POST':
        form = ImageFaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_path_face = form.instance.image.url
            result_nnface = nnface(image_path_face)
            return render(request, template, {"form": form, "img_obj_face": result_nnface})

    else:
        form = ImageFaceForm
        context = {
            'form': form
        }
    return render(request, template, context)


def ImageRubbish_upload_view(request):
    template = 'cam.html'
    if request.method == 'POST':
        form = ImageRubbishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_path_rubbish = form.instance.image.url
            result_nnrubbish = nnrubbish(image_path_rubbish)
            return render(request, template, {"form": form, "img_obj_rubbish": result_nnrubbish})

    else:
        form = ImageRubbishForm
    return render(request, template, {'form': form})


def jup(request):
    template = 'jup.html'
    return render(request, template)


def main(request):
    template = 'main.html'
    return render(request, template)


def team(request):
    template = 'team.html'
    return render(request, template)


def mat(request):
    template = 'mat.html'
    return render(request, template)

