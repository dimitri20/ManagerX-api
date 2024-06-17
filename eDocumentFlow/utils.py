from .models import Document


def document_is_verified_by_everyone(document: Document) -> bool:
    have_to_verify_users = document.have_to_verify_users.all()
    verified_by_users = document.verified_by_users.all()
    return set(have_to_verify_users).issubset(set(verified_by_users))


def document_is_signed_by_everyone(document: Document) -> bool:
    have_to_sign_users = document.have_to_sign_users.all()
    signed_by_users = document.signed_by_users.all()
    return set(have_to_sign_users).issubset(set(signed_by_users))
