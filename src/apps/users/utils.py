from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def send_email(current_site, user, to_email):
    # current_site = get_current_site(request)
    # mail_subject = 'Activation link has been sent to your email id'
    # message = render_to_string('acc_active_email.html', {
    #     'user': user,
    #     'domain': current_site,
    #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #     'token': account_activation_token.make_token(user),
    # })
    # email = send_mail(
    #     mail_subject, message, to=[to_email]
    # )
    # email.send()

    subject = 'Activation link has been sent to your email id'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'HTTP_PROTOCOL': settings.HTTP_PROTOCOL
    })
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email, ]
    send_mail(subject, message, email_from, recipient_list)
    return True
