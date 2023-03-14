from ..department import department_namespace
from flask_restx import fields


department_model = department_namespace.model(
    name="Department Details",
    model={
        "id": fields.Integer(description="Department ID"),
        "name": fields.String(required=True, description="Department Name"),
        "code": fields.String(required=True, description="Course Code"),
        "created_on": fields.DateTime(description="Created Date"),
        "created_by": fields.String(description="Creator's Username"),
        "modified_on": fields.DateTime(description="Modified Date"),
        "modified_by": fields.String(description="Modifier's Username"),
    }
)
