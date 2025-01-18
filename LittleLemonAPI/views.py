from django.shortcuts import render
from django.contrib.auth.models import User,Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsManager, IsCustomer,IsDeliveryCrew
from rest_framework.decorators import permission_classes
from .serializers import UserSerializer,OrderSerializer, OrderItemSerializer
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer,CartSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied

class ManagerGroupView(APIView):
    permission_classes=[IsAuthenticated,IsManager]
    #  get list of all managers, if u r manager then it allows you
    def get(self,request):
        '''We have to return all manager users '''
        managerGroup =Group.objects.get(name='manager')
        manager_users=managerGroup.user_set.all()
        serializer=UserSerializer(manager_users, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        """Add a user to the manager group."""
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.add(user)
            return Response({"message": "User added to manager group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DeliveryCrewGroupView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        """List all users in the delivery-crew group."""
        delivery_group = Group.objects.get(name='delivery-crew')
        delivery_crew = delivery_group.user_set.all()
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a user to the delivery-crew group."""
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
            delivery_group = Group.objects.get(name='delivery-crew')
            delivery_group.user_set.add(user)
            return Response({"message": "User added to delivery crew group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveManagerView(APIView):
    """
    Remove a user from the manager group.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            manager_group = Group.objects.get(name='manager')
            manager_group.user_set.remove(user)
            return Response({"message": "User removed from manager group"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Manager group not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemoveDeliveryCrewView(APIView):
    """
    Remove a user from the delivery-crew group.
    """
    permission_classes = [IsAuthenticated, IsManager]

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            delivery_group = Group.objects.get(name='delivery-crew')
            delivery_group.user_set.remove(user)
            return Response({"message": "User removed from delivery crew group"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Delivery crew group not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
# for menu items endpoins
class MenuItemListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Fetch all menu items
        menu_items = MenuItem.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2  # Set items per page
        paginated_menu_items = paginator.paginate_queryset(menu_items, request)

        # Serialize the paginated data
        serializer = MenuItemSerializer(paginated_menu_items, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Only manager can add new menu items
        if request.user.groups.filter(name="manager").exists():
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

class MenuItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, menuItem):
        try:
            # Fetch the menu item by its ID
            menu_item = MenuItem.objects.get(id=menuItem)
        except MenuItem.DoesNotExist:
            return Response(
                {"detail": "Menu item not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # If the user is authenticated, allow access
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, menuItem):
        # Only manager can update the menu item
        try:
            menu_item = MenuItem.objects.get(id=menuItem)
        except MenuItem.DoesNotExist:
            return Response({"detail": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.groups.filter(name="manager").exists():
            serializer = MenuItemSerializer(menu_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, menuItem):
    # Retrieve the menu item by ID
        try:
            menu_item = MenuItem.objects.get(id=menuItem)
        except MenuItem.DoesNotExist:
            return Response({"detail": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only allow managers to perform the update
        if request.user.groups.filter(name="manager").exists():
            serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)  # Use partial=True for partial updates
            if serializer.is_valid():
                serializer.save()  # Save the updated fields only
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, menuItem):
        # Only manager can delete a menu item
        try:
            menu_item = MenuItem.objects.get(id=menuItem)
        except MenuItem.DoesNotExist:
            return Response({"detail": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.groups.filter(name="manager").exists():
            menu_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Permission Denied."}, status=status.HTTP_403_FORBIDDEN)
    
class CartManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET: Fetch all cart items for the authenticated user.
        """
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        POST: Add a menu item to the cart for the authenticated user.
        """
        try:
            # Extract menu_item ID and quantity from the request
            menu_item_id = request.data.get('menu_item')
            quantity = request.data.get('quantity')

            # Validate the inputs
            if not menu_item_id or not quantity:
                return Response(
                    {"error": "Both 'menu_item' and 'quantity' are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Fetch the MenuItem object
            menu_item = MenuItem.objects.get(id=menu_item_id)

            # Calculate unit_price and total price
            unit_price = menu_item.price
            total_price = unit_price * int(quantity)

            # Create a new cart entry
            cart_item = Cart.objects.create(
                user=request.user,
                menu_item=menu_item,
                quantity=quantity,
                unit_price=unit_price,
                price=total_price
            )

            # Serialize the cart item
            serializer = CartSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "'quantity' must be a valid integer."},
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request):
        """
        DELETE: Remove all cart items for the authenticated user.
        """
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check user role
        user = request.user
        if user.groups.filter(name="customer").exists():
            # Customer: Return only their orders
            orders = Order.objects.filter(user=user)
        elif user.groups.filter(name="manager").exists():
            # Manager: Return all orders
            orders = Order.objects.all()
        elif user.groups.filter(name="delivery-crew").exists():
            # Delivery Crew: Return orders assigned to them
            orders = Order.objects.filter(delivery_crew=user)
        else:
            # If user does not belong to any role, return an empty response
            return Response({"detail": "No access for your role!"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty!"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.price for item in cart_items)
        order = Order.objects.create(user=request.user, total=total)

        order_items = [
            OrderItem(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()

        return Response({"detail": "Order created successfully!"}, status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, orderId):
        """GET request - For customers to view their orders"""
        try:
            order = Order.objects.get(id=orderId, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found or doesn't belong to the current user."}, status=status.HTTP_404_NOT_FOUND)

        order_items = OrderItem.objects.filter(order=order)
        order_items_data = OrderItemSerializer(order_items, many=True).data

        return Response({
            "order": OrderSerializer(order).data,
            "order_items": order_items_data
        }, status=status.HTTP_200_OK)

    def put(self, request, orderId):
        """PUT request - Manager can update order status and assign a delivery crew"""
        if not request.user.groups.filter(name="manager").exists():
            raise PermissionDenied("Only managers can update orders.")

        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        delivery_crew = request.query_params.get("delivery_crew")  # Extract from query parameters
        status_code = request.query_params.get("status")  # Extract from query parameters

        # Validate delivery_crew
        if delivery_crew:
            try:
                delivery_crew_user = User.objects.get(id=int(delivery_crew))
                order.delivery_crew = delivery_crew_user
            except User.DoesNotExist:
                return Response({"detail": "Delivery crew user not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and update status
        if status_code:
            try:
                status_code = int(status_code)  # Convert to integer
                if status_code not in (0, 1):
                    return Response({"detail": "Invalid status. Status must be 0 (out for delivery) or 1 (delivered)."},
                                    status=status.HTTP_400_BAD_REQUEST)
                order.status = status_code
            except ValueError:
                return Response({"detail": "Invalid status. Status must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        order.save()

        return Response({"detail": "Order updated successfully."}, status=status.HTTP_200_OK)

    def patch(self, request, orderId):
        """PATCH request - Delivery crew updates order status to 0 or 1"""
        if not request.user.groups.filter(name="Delivery crew").exists():
            raise PermissionDenied("Only delivery crew can update the order status.")

        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate if delivery crew is assigned
        if order.delivery_crew != request.user:
            return Response({"detail": "This order is not assigned to you."}, status=status.HTTP_400_BAD_REQUEST)

        status_code = request.data.get("status")

        # Validate status
        if status_code not in [0, 1]:
            return Response({"detail": "Invalid status. Status must be 0 (out for delivery) or 1 (delivered)."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the order status
        order.status = status_code
        order.save()

        return Response({"detail": "Order status updated successfully."}, status=status.HTTP_200_OK)

    def delete(self, request, orderId):
        """DELETE request - manager deletes an order"""
        if not request.user.groups.filter(name="manager").exists():
            raise PermissionDenied("Only managers can delete orders.")

        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete order and related order items
        order.delete()

        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)