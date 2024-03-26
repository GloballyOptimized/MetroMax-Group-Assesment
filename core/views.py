from django.shortcuts import render, redirect , get_object_or_404
from core.models import Product,Account,Customer,Book,Blog,Comment,Category,Shipment, Cargo, Tracking
from core.forms import ProductForm,CommentForm,ReviewForm,CategoryForm
from django.http import JsonResponse


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

#...............................................................................................................................

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(post=blog)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('blog_detail', blog_id=blog_id)
    else:
        form = CommentForm()
    
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'form': form})

#................................................................................................................................

def book_list(request):
    author_name = request.GET.get('author_name')
    books = Book.objects.all()

    if author_name:
        books = books.filter(author__name__icontains=author_name)

    return render(request, 'book_list.html', {'books': books, 'author_name': author_name})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = ReviewForm.objects.filter(book=book)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book_id)
    else:
        form = ReviewForm()

    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews, 'form': form})


#......................................................................................................................

def create_or_update_account(request):
    account_number = request.POST.get('account_number')
    balance = request.POST.get('balance')
    account_type = request.POST.get('account_type')

    if account_number and balance and account_type:
        account_number,created = Account.objects.update_or_create(
            account_number=account_number,
            defaults={'balance': balance, 'account_type': account_type}
        )
        if created:
            message = 'Account created successfully.'
        else:
            message = 'Account updated successfully.'
        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Missing account details.'})
    

def customer_form(request):
    account_type = request.GET.get('account_type')
    account_number = request.GET.get('account_number')

    customers = Customer.objects.all()

    if account_type:
        customers = customers.filter(accounts__account_type=account_type)
    if account_number:
        customers = customers.filter(accounts__account_number__icontains=account_number)

    return render(request, 'customer_form.html', {'customers': customers, 'account_type': account_type, 'account_number': account_number})


from .models import Shipment

def create_shipment(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        expected_delivery_date = request.POST.get('expected_delivery_date')

        if origin and destination and expected_delivery_date:
            shipment = Shipment(
                origin=origin,
                destination=destination,
                expected_delivery_date=expected_delivery_date
            )
            shipment.save()
            return redirect('shipment_list')

    return render(request, 'create_shipment.html')

def delete_shipment(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    shipment.delete()
    return redirect('shipment_list')

def shipment_list(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    status = request.GET.get('status')

    shipments = Shipment.objects.all()

    if origin:
        shipments = shipments.filter(origin__icontains=origin)
    if destination:
        shipments = shipments.filter(destination__icontains=destination)
    if status:
        shipments = shipments.filter(status=status)

    return render(request, 'shipment_list.html', {'shipments': shipments})


def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    cargo_items = Cargo.objects.filter(shipment=shipment)
    tracking = Tracking.objects.filter(shipment=shipment).first()

    return render(request, 'shipment_detail.html', {'shipment': shipment, 'cargo_items': cargo_items, 'tracking': tracking})