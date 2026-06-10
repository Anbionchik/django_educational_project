from main.models import ListModel
from Khlopkov.settings import MIN_ELEMENTS, PAGE_COUNT
from django.shortcuts import render, reverse, redirect
from main.forms import ListForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse


@login_required(login_url='registration/login/')
def main_view(request):
    """ Главная View """
    user = request.user

    try:
        lists = ListModel.objects.filter(
            user=user,
        ).order_by(
            '-created'
        )
    except TypeError:
        lists = []

    paginator = Paginator(lists, PAGE_COUNT)
    page = request.GET.get('page')

    try:
        list_page = paginator.page(page)
    except PageNotAnInteger:
        list_page = paginator.page(1)
    except EmptyPage:
        list_page = paginator.page(paginator.num_pages)

    context = {
        'lists': list_page,
        'user': request.user.username,
        'pages': list(paginator.page_range),
        'page_obj': paginator.get_page(page),
        'min_elements': MIN_ELEMENTS
    }
    return render(request, 'index.html', context)


def min_elements():
    return MIN_ELEMENTS


def edit_view(request, pk):

    obj = ListModel.objects.filter(id=pk).first()

    if request.method == "POST":

        name = request.POST.get('name')
        user = request.user

        form = ListForm({
            'name': name,
            'user': user
        })

        success_url = reverse('main:main')
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.save()
            return redirect(success_url)
    else:
        form = ListForm(instance=obj)
    return render(request, "main_new_list.html", {'form': form})


def new_list_view(request):

    form = ListForm()

    if request.method == "POST":
        name = request.POST.get('name')
        form = ListForm({
            'name': name,
            'user': request.user
        })
        success_url = reverse('main:main')
        if form.is_valid():
            form.save()
            return redirect(success_url)

    return render(request, "main_new_list.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:main')


def delete_view(request, pk):
    if request.method == 'POST':
        list_item = ListModel.objects.filter(id=pk).first()
        if list_item:
            list_item.delete()
            return HttpResponse(status=201)
    return Http404
