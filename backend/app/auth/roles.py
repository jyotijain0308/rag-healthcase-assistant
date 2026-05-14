from enum import Enum

class UserRole(str, Enum):

    ADMIN = "admin"

    DOCTOR = "doctor"

    NURSE = "nurse"

    AUDITOR = "auditor"

    PATIENT = "patient"