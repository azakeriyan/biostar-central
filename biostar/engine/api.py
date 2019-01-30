
import hjson
import logging
import os

from django.conf import settings
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from biostar.engine.models import Analysis, Project, image_path
from biostar.utils.shortcuts import reverse
from biostar.engine.decorators import require_api_key


logger = logging.getLogger("engine")


def change_image(request, obj):

    placeholder = os.path.join(settings.STATIC_ROOT, "images", "placeholder.png")
    img_path = placeholder if not obj.image else obj.image.path
    file_object = request.data.get("file", "")

    if request.method == "PUT" and file_object:

        if not obj.image:
            img_path = os.path.join(settings.MEDIA_ROOT,image_path(instance=obj, filename=img_path))
            obj.image.save(name=img_path, content=file_object)
        else:
            open(img_path, "wb").write(file_object.read())

    img_stream = open(img_path, "rb").read()
    return HttpResponse(content=img_stream, content_type="image/jpeg")


@api_view(['GET'])
def project_api_list(request):

    projects = Project.objects.get_all()
    api_key = request.GET.get("k", "")

    # Only show public projects when api key is not correct or provided.
    if settings.API_KEY != api_key:
        projects = projects.filter(privacy=Project.PUBLIC)

    payload = dict()
    for project in projects:
        payload.setdefault(project.uid, dict()).update(
                            name=project.name,
                            recipes={recipe.uid:
                                     dict(name=recipe.name,
                                          json=reverse("recipe_api_json", kwargs=dict(uid=recipe.uid)),
                                          template=reverse("recipe_api_template", kwargs=dict(uid=recipe.uid)))
                                     for recipe in project.analysis_set.all()
                                     },
                            privacy=dict(Project.PRIVACY_CHOICES)[project.privacy],
                            )

    return Response(data=payload, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@require_api_key(type=Project)
def project_info(request, uid):
    """
    GET request : return project info as json data
    PUT request : change project info using json data
    """

    project = Project.objects.get_all(uid=uid).first()

    if request.method == "PUT":
        file_object = request.data.get("file", "")
        conf = hjson.load(file_object)
        if file_object:
            project.name = conf.get("settings", {}).get("name") or project.name
            project.text = conf.get("settings", {}).get("text") or project.text
            project.save()

    payload = hjson.loads(project.json_text)
    return Response(data=payload, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@require_api_key(type=Project)
def project_image(request, uid):
    """
    GET request : return project image
    PUT request : change project image
    """
    project = Project.objects.filter(uid=uid).first()

    return change_image(request, obj=project)


@api_view(['GET', 'PUT'])
@require_api_key(type=Analysis)
def recipe_image(request, uid):
    """
    GET request: Return recipe image.
    PUT request: Updates recipe image with given file.
    """

    recipe = Analysis.objects.filter(uid=uid).first()

    return change_image(request, obj=recipe)


@api_view(['GET'])
def recipe_api_list(request):

    recipes = Analysis.objects.get_all()
    api_key = request.GET.get("k", "")

    # Only show public recipes when api key is not correct or provided.
    if settings.API_KEY != api_key:
        recipes = recipes.filter(project__privacy=Project.PUBLIC)

    payload = dict()
    for recipe in recipes:
        payload.setdefault(recipe.uid, dict()).update(
                            name=recipe.name,
                            json=reverse("recipe_api_json", kwargs=dict(uid=recipe.uid)),
                            template=reverse("recipe_api_template", kwargs=dict(uid=recipe.uid)),
                            privacy=dict(Project.PRIVACY_CHOICES)[recipe.project.privacy],
                            project_uid=recipe.project.uid,
                            project_name=recipe.project.name)

    return Response(data=payload, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@require_api_key(type=Analysis)
def recipe_json(request, uid):
    """
    GET request: Returns recipe json
    PUT request: Updates recipe json with given file.
    """
    recipe = Analysis.objects.filter(uid=uid).first()

    if request.method == "PUT":
        # Get the new json that will replace the current one
        file_object = request.data.get("file", "")
        updated_json = hjson.load(file_object)
        recipe.json_text = hjson.dumps(updated_json) if file_object else recipe.json_text

        # Update help and name in recipe from json.
        if updated_json.get("settings"):
            recipe.name = updated_json["settings"].get("name", recipe.name)
            recipe.text = updated_json["settings"].get("help", recipe.text)

        recipe.save()

    payload = recipe.json_data

    return Response(data=payload, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@require_api_key(type=Analysis)
def recipe_template(request, uid):
    """
    GET request: Returns recipe template
    PUT request: Updates recipe template with given file.
    """

    recipe = Analysis.objects.filter(uid=uid).first()

    # API key is always checked by @require_api_key decorator.
    if request.method == "PUT":
        # Get the new template that will replace the current one
        file_object = request.data.get("file", "")
        stream = file_object.read().decode("utf-8")
        recipe.template = stream if file_object else recipe.template
        recipe.save()
    payload = recipe.template

    return HttpResponse(content=payload, content_type="text/plain")

