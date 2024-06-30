from .models import Document, TaskRegisteringEvent, SendDocumentToVerifyEvent, SendDocumentToSignEvent


def document_is_verified_by_everyone(document: Document) -> bool:
    have_to_verify_users = document.have_to_verify_users.all()
    verified_by_users = document.verified_by_users.all()
    return set(have_to_verify_users).issubset(set(verified_by_users))


def document_is_signed_by_everyone(document: Document) -> bool:
    have_to_sign_users = document.have_to_sign_users.all()
    signed_by_users = document.signed_by_users.all()
    return set(have_to_sign_users).issubset(set(signed_by_users))


def filter_documents_by_sender_and_receiver(request):
    queries = request.query_params
    queryset = Document.objects.all()
    if "task" in queries:

        match queries['task']:
            case TaskRegisteringEvent.TaskType.VERIFY:
                if "sent_by_user" in queries:
                    verify_sent_by_user = SendDocumentToVerifyEvent.objects.all().filter(
                        sender__id=queries['sent_by_user'])
                    verify_sent_by_user_document_ids = verify_sent_by_user.values_list('document', flat=True)
                    queryset = Document.objects.filter(uuid__in=verify_sent_by_user_document_ids)
                elif "received_to_user" in queries:
                    verify_received_to_user = SendDocumentToVerifyEvent.objects.all().filter(
                        recipient__id=queries['received_to_user'])
                    verify_received_to_user_document_ids = verify_received_to_user.values_list('document',
                                                                                               flat=True)
                    queryset = Document.objects.filter(uuid__in=verify_received_to_user_document_ids)

            case TaskRegisteringEvent.TaskType.SIGN:
                if "sent_by_user" in queries:
                    sign_sent_by_user = SendDocumentToSignEvent.objects.all().filter(
                        sender__id=queries['sent_by_user'])
                    sign_sent_by_user_document_ids = sign_sent_by_user.values_list('document', flat=True)
                    queryset = Document.objects.filter(uuid__in=sign_sent_by_user_document_ids)

                elif "received_to_user" in queries:
                    sign_received_to_user = SendDocumentToSignEvent.objects.all().filter(
                        recipient__id=queries['received_to_user'])
                    sign_received_to_user_document_ids = sign_received_to_user.values_list('document', flat=True)
                    queryset = Document.objects.filter(uuid__in=sign_received_to_user_document_ids)

    return queryset
