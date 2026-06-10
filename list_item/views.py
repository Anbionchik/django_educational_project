from django.shortcuts import render, redirect, reverse
from main.models import ListModel
from list_item.models import ListItemModel
from django.http import Http404, HttpResponse
from list_item.forms import ListItemForm
from django.contrib.auth.decorators import login_required
from Khlopkov.settings import MIN_ELEMENTS, PAGE_COUNT
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


@login_required(login_url='/')
def list_item_view(request, pk):

    user = request.user

    # Список со значениями для списка задач в шаблоне

    lists = ListItemModel.objects.filter(
        listmodel_id=pk
    ).order_by(
        'created'
    )

    # список из main.view

    main_list = ListModel.objects.filter(id=pk)

    header = main_list.values_list(
        'name',
        flat=True
    ).first()

    user_verification = main_list.values_list('user__username', flat=True).first()

    if user_verification != str(user):
        raise Http404

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
        'header': header,
        'list_pk': pk,
        'pages': list(paginator.page_range),
        'page_obj': paginator.get_page(page),
        'min_elements': MIN_ELEMENTS

    }
    return render(request, 'list.html', context)


def new_list_item_view(request, pk):

    form = ListItemForm()

    if request.method == "POST":
        name = request.POST.get('name')
        expiration_date = request.POST.get('expiration_date')
        form = ListItemForm({
            'name': name,
            'expiration_date': expiration_date,
            'listmodel_id': pk
        })
        success_url = reverse('main:list', kwargs={'pk': pk})
        if form.is_valid():
            form.save()
            return redirect(success_url)

    return render(request, "item_new_list.html", {'form': form, 'primary_key': pk})


def edit_view(request, pk):

    obj = ListItemModel.objects.filter(id=pk).first()
    back_address = obj.listmodel_id_id

    if request.method == "POST":

        name = request.POST.get('name')
        expiration_date = request.POST.get('expiration_date')
        listmodel_id = obj.listmodel_id

        form = ListItemForm({
            'name': name,
            'listmodel_id': listmodel_id,
            'expiration_date': expiration_date
        })

        success_url = reverse('main:list', kwargs={'pk': back_address})
        if form.is_valid():
            obj.name = form.cleaned_data['name']
            obj.expiration_date = form.cleaned_data['expiration_date']
            obj.save()
            return redirect(success_url)
    else:
        form = ListItemForm(instance=obj)
    return render(request, "item_new_list.html", {'form': form, 'primary_key': back_address})


def done_view(request):
    data = json.loads(request.body.decode())
    pk = int(data['id'])
    list_item = ListItemModel.objects.get(id=pk)
    value = not list_item.is_done
    list_item.is_done = value
    list_item.save()
    return HttpResponse(status=201)


def all_done_view(request):
    data = json.loads(request.body.decode())
    pk = int(data['id'])
    list_items = ListItemModel.objects.filter(listmodel_id=pk)
    list_items.update(is_done=True)
    main_list = ListModel.objects.get(id=pk)
    main_list.is_done = True
    main_list.save()
    return HttpResponse(status=201)
