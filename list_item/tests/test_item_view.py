import pytest
from django.shortcuts import reverse
from list_item.models import ListItemModel

TEST_CLIENT = {
    'username': 'TestUser',
    'email': '123@123.ru',
    'password': 'q1w2e3r4TT',
}


def test_list_item_page_return_correct_html(client, new_client, new_list):
    """
    Проверка что рендерится правильный шаблон списка дел
    """
    list_item = ListItemModel.objects.create(
        name='Какое то дело',
        listmodel_id=new_list
    )
    client.login(username=new_client.username, password=TEST_CLIENT['password'])
    response = client.get(reverse('main:list', kwargs={'pk': list_item.id}))
    # response = client.get(reverse('list_item:list_item', kwargs={'pk': list_item.id}))
    html = response.content.decode('utf8')
    assert response.status_code == 200
    assert "<title>Список</title>" in html
    assert f"<div class=\"table-data_table-header-item-1\">{new_list.name}</div>" in html
    assert html.strip().endswith('</html>')
    assert 'list.html' in [t.name for t in response.templates]
