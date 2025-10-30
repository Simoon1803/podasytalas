from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def custom_login(request):
    # Si ya está logueado, no le vuelvas a pedir login. Lo mandas directo al dashboard.
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Permitimos SOLO usuarios con acceso al panel
            if not user.is_staff:
                messages.error(request, "❌ No tienes permiso para acceder al panel administrativo.")
                return render(request, "registration/login.html", {
                    "form": {
                        "username": {"value": username},
                        "errors": True
                    }
                })

            # Logea al usuario
            login(request, user)
            return redirect('dashboard:home')
        else:
            # Credenciales malas
            messages.error(request, "❌ Usuario o contraseña incorrectos.")

            # Le devolvemos de nuevo el username para que no tenga que escribirlo otra vez
            return render(request, "registration/login.html", {
                "form": {
                    "username": {"value": username},
                    "errors": True
                }
            })

    # GET normal: mostrar formulario vacío
    return render(request, "registration/login.html", {
        "form": {
            "errors": False
        }
    })
