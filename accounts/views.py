from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, DematAccount, Transaction, CarbonCreditType

# ---------------- LANDING ----------------
def landing(request):
    return render(request, 'landing.html')

# ---------------- LOGIN ----------------
def user_login(request):
    msg = ""
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            msg = "Invalid credentials"
    return render(request, 'login.html', {'msg': msg})

# ---------------- REGISTER ----------------
def register(request):
    msg = ""
    if request.method == "POST":
        if User.objects.filter(username=request.POST['username']).exists():
            msg = "User already registered"
        else:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password']
            )
            profile = user.profile
            profile.role = request.POST['role']
            profile.is_approved = False
            profile.save()
            msg = "Registration successful. Approval pending."
    return render(request, 'register.html', {'msg': msg})

# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    demat = DematAccount.objects.get(user=request.user)

    # ---------------- APPROVAL PENDING ----------------
    if not profile.is_approved:
        return render(request, "dashboard.html", {
            "pending": True,
            "profile": profile
        })

    # ================= SELLER DASHBOARD =================
    if profile.role == "SELLER":

        # Add credits
        if request.method == "POST" and "add_credits" in request.POST:
            qty = float(request.POST.get("add_credits"))
            demat.credit_balance += qty
            demat.save()

        transactions = Transaction.objects.filter(
            seller=request.user
        ).order_by("-date")

        return render(request, "dashboard.html", {
            "seller": True,
            "profile": profile,
            "demat": demat,
            "transactions": transactions
        })

    # ================= BUYER DASHBOARD =================
    if profile.role == "BUYER":

        sellers = DematAccount.objects.filter(
            user__profile__role="SELLER",
            user__profile__is_approved=True,
            credit_balance__gt=0
        )

        # Handle BUY
        if request.method == "POST" and "buy_from" in request.POST:
            seller_demat_id = request.POST.get("buy_from")
            credits = int(request.POST.get("credits"))

            seller_demat = DematAccount.objects.get(id=seller_demat_id)

            # Get default credit type
            credit_type = CarbonCreditType.objects.first()
            if not credit_type:
                raise Exception("No CarbonCreditType found. Add one from admin.")

            price = credit_type.price_per_credit
            amount = credits * price

            if seller_demat.credit_balance >= credits:
                # Seller update
                seller_demat.credit_balance -= credits
                seller_demat.wallet_balance += amount
                seller_demat.save()

                # Buyer update
                demat.credit_balance += credits
                demat.wallet_balance -= amount
                demat.save()

                # Save transaction
                Transaction.objects.create(
                    buyer=request.user,
                    seller=seller_demat.user,
                    credits=credits,
                    amount=amount,
                    credit_type=credit_type
                )

        transactions = Transaction.objects.filter(
            buyer=request.user
        ).order_by("-date")

        return render(request, "dashboard.html", {
            "buyer": True,
            "profile": profile,
            "demat": demat,
            "transactions": transactions,
            "sellers": sellers
        })

# ---------------- BUY CREDITS ----------------
@login_required
def buy(request):
    if request.method == "POST":
        seller = User.objects.get(id=request.POST['seller'])
        credits = float(request.POST['credits'])

        buyer_demat = DematAccount.objects.get(user=request.user)
        seller_demat = DematAccount.objects.get(user=seller)

        credit_type = CarbonCreditType.objects.first()
        amount = credits * credit_type.price_per_credit

        if seller_demat.credit_balance >= credits:
            seller_demat.credit_balance -= credits
            seller_demat.wallet_balance += amount
            buyer_demat.credit_balance += credits

            seller_demat.save()
            buyer_demat.save()

            credit_type = CarbonCreditType.objects.first()

            Transaction.objects.create(
                buyer=request.user,
                seller=seller_demat.user,
                credits=credits,
                amount=amount,
                credit_type=credit_type
            )

    return redirect('dashboard')
