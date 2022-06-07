from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from website.models import *
from website.forms import *
from datetime import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.db import connection
from django.contrib.auth.forms import UserCreationForm
cursor = connection.cursor()

def year():
    return f"2020 - {datetime.now().year}" if datetime.now().year != 2020 else "2020"

def fettolist():
    results = cursor.fetchall()
    x = cursor.description
    resultsList = []
    for r in results:
        i = 0
        d = {}
        while i < len(x):
            d[x[i][0]] = r[i]
            i = i + 1
        resultsList.append(d)
    return resultsList

def index(request):
    return render(request, "index.html", {
        "club": clubmodel.objects.first(),
        "title": "Página Principal",
        "year": year()
    })

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "club": clubmodel.objects.first(),
        "title": "Painel Principal",
        "players_count": len(Group.objects.raw("SELECT * FROM auth_user_groups INNER JOIN auth_group ON group_id = auth_group.id WHERE auth_group.name = 'Jogador'")),
        "coachs_count": len(Group.objects.raw("SELECT * FROM auth_user_groups INNER JOIN auth_group ON group_id = auth_group.id WHERE auth_group.name = 'Treinador'")),
        "games_count": gamemodel.objects.count(),
        "trainings_count": trainingmodel.objects.count(),
        "trainings": trainingmodel.objects.raw("SELECT * FROM website_trainingmodel ORDER BY id DESC"),
        "games": gamemodel.objects.raw("SELECT * FROM website_gamemodel ORDER BY id DESC"),
    })

@login_required
def profiles(request):
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST["action"] == "delete":
                request.user.delete()
                return HttpResponseRedirect(reverse("index"))
            elif request.POST["action"] == "edit":
                temp = User.objects.get(id=request.user.id)
                temp.first_name = request.POST["first_name"]
                temp.last_name = request.POST["last_name"]
                temp.email = request.POST["email"]
                temp.profile.bio = request.POST["bio"]
                temp.profile.born = request.POST["born"]
                temp.save()
                return HttpResponseRedirect(reverse("profile"))
    data = {}
    cursor.execute("SELECT * FROM auth_group")
    data["groups"] = fettolist()
    cursor.execute("SELECT * FROM auth_user INNER JOIN website_profile ON auth_user.id=user_id WHERE auth_user.id = %s", [request.user.id])
    data["userinfo"] = fettolist()[0]
    return render(request, "profile.html", {
        "title": "Perfil",
        "club": clubmodel.objects.raw("SELECT * FROM website_clubmodel LIMIT 1")[0],
        "breadcrumb_title": "Perfil do Utilizador",
        "data": data
    })

@login_required
def trainings(request):
    search = None
    if "search" in request.GET:
        search = trainingmodel.objects.raw("SELECT * FROM website_trainingmodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"])
        search.quant = len(trainingmodel.objects.raw("SELECT * FROM website_trainingmodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"]))
    if request.method == "POST":
        if len(request.user.groups.raw("SELECT auth_group.id, auth_group.name FROM auth_group INNER JOIN auth_user_groups ON (auth_group.id = auth_user_groups.group_id) WHERE (auth_user_groups.user_id = %s AND auth_group.name IN ('Treinador', 'Administrador'))", [request.user.id])):
            if "action" in request.POST:
                if request.POST["action"] == "edit":
                    cursor.execute("UPDATE website_trainingmodel SET name = %s, start = %s, end = %s, team_id = %s WHERE id = %s", [request.POST["name"], request.POST["start"], request.POST["end"], request.POST["team"], request.POST["id"]])
                elif request.POST["action"] == "delete":
                    cursor.execute("DELETE FROM website_trainingmodel WHERE id = %s", [request.POST["id"]])
            else:
                form = trainingform(request.POST)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse("training"))
    return render(request, "training.html", {
        "title": "Treinos",
        "club": clubmodel.objects.first(),
        "breadcrumb_title": "Treinos",
        "teams": clubmodel.objects.raw("SELECT * FROM website_teammodel"),
        "trainings": Paginator(trainingmodel.objects.raw("SELECT * FROM website_trainingmodel ORDER BY id DESC"), 10).get_page(request.GET.get("page")),
        "count": len(trainingmodel.objects.raw("SELECT * FROM website_trainingmodel")),
        "search": search
    })

@login_required
def games(request):
    search = None
    if "search" in request.GET:
        search = gamemodel.objects.raw("SELECT * FROM website_gamemodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"])
        search.quant = len(gamemodel.objects.raw("SELECT * FROM website_gamemodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"]))
    if request.method == "POST":
        if len(request.user.groups.raw("SELECT auth_group.id, auth_group.name FROM auth_group INNER JOIN auth_user_groups ON (auth_group.id = auth_user_groups.group_id) WHERE (auth_user_groups.user_id = %s AND auth_group.name IN ('Treinador', 'Administrador'))",[request.user.id])):
            if "action" in request.POST:
                if request.POST["action"] == "edit":
                    cursor.execute(
                        "UPDATE website_gamemodel SET name = %s, start = %s, end = %s, team_id = %s, teamgoals = %s, enemygoals = %s  WHERE id = %s",
                        [request.POST["name"], request.POST["start"], request.POST["end"], request.POST["team"],
                         request.POST["teamgoals"], request.POST["enemygoals"], request.POST["id"]])
                elif request.POST["action"] == "delete":
                    cursor.execute("DELETE FROM website_gamemodel WHERE id = %s", [request.POST["id"]])
            else:
                form = gameform(request.POST)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse("game"))
    return render(request, "game.html", {
        "title": "Jogos",
        "club": clubmodel.objects.first(),
        "breadcrumb_title": "Jogos",
        "teams": clubmodel.objects.raw("SELECT * FROM website_teammodel"),
        "games": Paginator(gamemodel.objects.raw("SELECT * FROM website_gamemodel ORDER BY id DESC"), 10).get_page(request.GET.get("page")),
        "count": len(gamemodel.objects.raw("SELECT * FROM website_gamemodel")),
        "search": search
    })

@login_required
def teams(request):
    search = None
    if "search" in request.GET:
        search = teammodel.objects.raw("SELECT * FROM website_teammodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"])
        search.quant = len(teammodel.objects.raw("SELECT * FROM website_teammodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"]))
    if request.method == "POST":
        if len(request.user.groups.raw("SELECT auth_group.id, auth_group.name FROM auth_group INNER JOIN auth_user_groups ON (auth_group.id = auth_user_groups.group_id) WHERE (auth_user_groups.user_id = %s AND auth_group.name = 'Administrador')", [request.user.id])):
            if "action" in request.POST:
                if request.POST["action"] == "edit":
                    cursor.execute("UPDATE website_teammodel SET name = %s, trainer_id = %s, echelon_id = %s WHERE id = %s", [request.POST["name"], request.POST["trainer"], request.POST["echelon"], request.POST["id"]])
                elif request.POST["action"] == "delete":
                    cursor.execute("DELETE FROM website_teammodel WHERE id = %s", [request.POST["id"]])
            else:
                form = teamform(request.POST)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse("team"))
    return render(request, "team.html", {
        "title": "Equipas",
        "club": clubmodel.objects.first(),
        "breadcrumb_title": "Equipas",
        "trainers": User.objects.raw("SELECT auth_user.* FROM auth_user INNER JOIN (auth_group INNER JOIN auth_user_groups ON auth_group.id = auth_user_groups.group_id) ON auth_user.id = auth_user_groups.user_id WHERE auth_group.name = 'Treinador'"),
        "echelons": clubmodel.objects.raw("SELECT * FROM website_echelonmodel"),
        "teams": Paginator(teammodel.objects.raw("SELECT * FROM website_teammodel ORDER BY id DESC"), 10).get_page(request.GET.get("page")),
        "count": len(gamemodel.objects.raw("SELECT * FROM website_teammodel")),
        "search": search
    })

@login_required
def echelons(request):
    search = None
    if "search" in request.GET:
        search = echelonmodel.objects.raw("SELECT * FROM website_echelonmodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"])
        search.quant = len(echelonmodel.objects.raw("SELECT * FROM website_echelonmodel WHERE name LIKE %s", ["%" + request.GET["search"] + "%"]))
    if request.method == "POST":
        if len(request.user.groups.raw("SELECT auth_group.id, auth_group.name FROM auth_group INNER JOIN auth_user_groups ON (auth_group.id = auth_user_groups.group_id) WHERE (auth_user_groups.user_id = %s AND auth_group.name = 'Administrador')", [request.user.id])):
            if "action" in request.POST:
                if request.POST["action"] == "edit":
                    cursor.execute("UPDATE website_echelonmodel SET name = %s WHERE id = %s", [request.POST["name"], request.POST["id"]])
                elif request.POST["action"] == "delete":
                    #cursor.execute("DELETE FROM website_echelonmodel WHERE id = %s", [request.POST["id"]])
                    echelonmodel.objects.get(id=request.POST["id"]).delete()
            else:
                form = echelonform(request.POST)
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(reverse("echelon"))
    return render(request, "echelon.html", {
        "title": "Escalões",
        "club": clubmodel.objects.first(),
        "breadcrumb_title": "Escalões",
        "echelons": Paginator(echelonmodel.objects.raw("SELECT * FROM website_echelonmodel ORDER BY name"), 10).get_page(request.GET.get("page")),
        "count": echelonmodel.objects.all().count(),
        "search": search
    })

@login_required
def club(request):
    if request.method == "POST":
        if len(request.user.groups.raw("SELECT auth_group.id, auth_group.name FROM auth_group INNER JOIN auth_user_groups ON (auth_group.id = auth_user_groups.group_id) WHERE (auth_user_groups.user_id = %s AND auth_group.name = 'Administrador')", [request.user.id])):
            if "action" in request.POST:
                if request.POST["action"] == "club":
                    cursor.execute("UPDATE website_clubmodel SET name = %s, description = %s, about = %s, contact = %s", [request.POST["name"], request.POST["description"], request.POST["about"], request.POST["contact"]])
                    if request.POST["image"] != "":
                        temp = clubmodel.objects.all()[0]
                        temp.image = request.FILES["image"]
                        temp.save()
                elif request.POST["action"] == "group":
                    if request.POST["group"] in ["Utilizador", "Jogador", "Treinador", "Administrador"]:
                        group = Group.objects.raw("SELECT * FROM auth_group WHERE name = %s LIMIT 1", [request.POST["group"]])[0].id
                        cursor.execute("UPDATE auth_user_groups SET group_id = %s WHERE user_id = %s", [group, request.POST["user"]])
                return HttpResponseRedirect(reverse("club"))
    return render(request, "club.html", {
        "title": "Gerir Clube",
        "club": clubmodel.objects.first(),
        "breadcrumb_title": "Clube",
        "User": User.objects.all()
    })

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("login"))
    return render(request, "registration/register.html", {
        "club": clubmodel.objects.first(),
        "form": form
    })