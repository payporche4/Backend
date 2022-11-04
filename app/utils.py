from django.utils.crypto import get_random_string
import uuid
import secrets


def generate_transaction_reference():
    return secrets.token_urlsafe(13).upper()


chars = "abcdeNOPQRSTUfghirstuvwxyz0123ABCDjklmnopqEFGHIJKL456x9MVWXYZ"


def unique_rand():
    while True:
        wallet_tag = get_random_string(16, chars.lower())
        return wallet_tag


def user_thumbnail_folder(instance, filename):
    return "%s/%s" % (instance.owner.id, filename)
