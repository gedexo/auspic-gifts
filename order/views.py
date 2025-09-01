from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.list import ListView

from products.models import ProductVariant

from .models import Wishlist


class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


# class AddToWishlistView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({"message": "User not authenticated"}, status=401)

#         user = self.request.user
#         product_id = request.GET.get("product_id", "")
#         product_varient = get_object_or_404(ProductVariant, id=product_id)
#         if not Wishlist.objects.filter(
#             user=user, product_varients=product_varient
#         ).exists():
#             # Create a new Wishlist object
#             Wishlist.objects.create(user=user, product_varients=product_varient)
#             return JsonResponse(
#                 {
#                     "message": "Product Added from Wishlist successfully",
#                     "wishlist_count": Wishlist.objects.filter(
#                         user=request.user
#                     ).count(),
#                 }
#             )
#         else:
#             return JsonResponse({"message": "Product is already in the Wishlist."})


# class RemoveFromWishlistView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         product_id = self.kwargs.get("product_id")
#         user = self.request.user

#         wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
#         wishlist_item.delete()

#         return JsonResponse(
#             {
#                 "message": "Product Removed from Wishlist successfully",
#                 "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
#             }
#         )



class AddToWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.GET.get("product_id", "")
        
        print(f"Received product_id: {product_id}")  # Debug line
        
        if not product_id:
            return JsonResponse({"message": "Product ID is required"}, status=400)
        
        try:
            product_varient = get_object_or_404(ProductVariant, pk=product_id)
            
            # Check if product is already in wishlist
            if not Wishlist.objects.filter(
                user=user, product_varients=product_varient
            ).exists():
                # Create a new Wishlist object
                Wishlist.objects.create(user=user, product_varients=product_varient)
                return JsonResponse(
                    {
                        "message": "Product added to wishlist successfully",
                        "wishlist_count": Wishlist.objects.filter(
                            user=request.user
                        ).count(),
                    }
                )
            else:
                return JsonResponse({"message": "Product is already in the wishlist."}, status=400)
        except ProductVariant.DoesNotExist:
            return JsonResponse({"message": "Product not found"}, status=404)
        except Exception as e:
            print(f"Error: {e}")  # Debug line
            return JsonResponse({"message": str(e)}, status=500)

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user
        
        if not product_id:
            return JsonResponse({"message": "Product ID is required"}, status=400)
        
        try:
            # This should look up by wishlist item ID, not product variant ID
            wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
            wishlist_item.delete()
            return JsonResponse(
                {
                    "message": "Product removed from wishlist successfully",
                    "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
                }
            )
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

# Alternative remove view if you want to remove by product variant ID
class RemoveFromWishlistByProductView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user
        
        if not product_id:
            return JsonResponse({"message": "Product ID is required"}, status=400)
        
        try:
            product_varient = get_object_or_404(ProductVariant, id=product_id)
            wishlist_item = get_object_or_404(Wishlist, user=user, product_varients=product_varient)
            wishlist_item.delete()
            return JsonResponse(
                {
                    "message": "Product removed from wishlist successfully",
                    "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
                }
            )
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)