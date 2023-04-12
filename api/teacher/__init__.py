from flask_restx import Namespace

teacher_namespace = Namespace(name="Teacher", description="Current Teacher Operations")

adm_teacher_namespace = Namespace(name="Teachers", description="Operations on Teachers (Admins Only)")