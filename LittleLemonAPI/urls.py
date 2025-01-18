from django.urls import path
from .views import (
    ManagerGroupView, DeliveryCrewGroupView,OrderView,OrderDetailView, RemoveManagerView, RemoveDeliveryCrewView,MenuItemListView,MenuItemDetailView,CartManagementView
)

urlpatterns = [
    # Manager group endpoints
    path('groups/manager/users/', ManagerGroupView.as_view(), name='manager-group'),
    path('groups/manager/users/<int:user_id>/', RemoveManagerView.as_view(), name='remove-manager'),

    # Delivery crew group endpoints, but auth as manager required
    path('groups/delivery-crew/users/', DeliveryCrewGroupView.as_view(), name='delivery-crew-group'),
    path('groups/delivery-crew/users/<int:user_id>/', RemoveDeliveryCrewView.as_view(), name='remove-delivery-crew'),
    
    # for getting menu items
    path('menu-items/', MenuItemListView.as_view(), name='menu_item_list'),
    # for list a single menu item anyone can do it but only managers can do other actions
    path('menu-items/<int:menuItem>/', MenuItemDetailView.as_view(), name='menu_item_detail'),
    # for cart managment
    path('cart/menu-items/', CartManagementView.as_view(), name='cart-management'),
     path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:orderId>/', OrderDetailView.as_view(), name='order_detail'),
]
