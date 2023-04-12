from flask_restx import Namespace

admin_namespace = Namespace(name="Admin", description="Operations on Admin (Admin Only).")
